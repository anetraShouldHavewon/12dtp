from flask import Flask, render_template, abort
import sqlite3

app = Flask(__name__)

# opening connection to sql database, evaluating if the query used is
# a fetchone or fetchall and returning the result of the query
# this function deals with getting data from the "Movie_Database_1.db"


def sql(fetch_status, query, constraint):
    conn = sqlite3.connect("Movie_Database_1.db")
    cur = conn.cursor()
    if constraint is None:
        if fetch_status == "fetchone":
            fetch_result = cur.execute(query).fetchone()
        if fetch_status == "fetchall":
            fetch_result = cur.execute(query).fetchall()
    else:
        if fetch_status == "fetchone":
            fetch_result = cur.execute(query, (constraint,)).fetchone()
        if fetch_status == "fetchall":
            fetch_result = cur.execute(query, (constraint,)).fetchall()

    return fetch_result
# ALL FUNCTIONS BEYOND THIS POINT TAKE DATA FETCHED FROM DATABASES AND PUTS
# THEM INTO MANAGEABLE LIST FORMS#


def fetch_all_result_list(query, constraint):
    return_list = []
    query_result = sql("fetchall", query, constraint)
    for item in query_result:
        return_list.append(item[0])
    return return_list


def genre_id_list_from_genre_name_list(genre_list):
    # getting a list of ids of genres from a list of genres names
    # and a alphabetically sorted capitalized list of genre names
    genre_id_list = []
    genre_list.sort()
    new_genre_list = []
    for genre_name in genre_list:
        genre_name_db = genre_name.title()
        genre_id = sql("fetchone", "SELECT id FROM Genre WHERE name = ?",
                       genre_name_db)[0]

        # evaluating if a genre is logged into in the database
        # if genre_id does not exist, the genre name in the list of genres is
        #  misspelt or does not exist in the database yet
        if genre_id is None:
            print("{} is invalid.\nMaybe the genre name is misspelt or this"
                  "genre does not yet exist in the database"
                  "yet.".format(genre_name_db))
        else:
            genre_id_list.append(genre_id)
        new_genre_list.append(genre_name_db)

    return [genre_id_list, new_genre_list]


def movie_gallery_info_from_movie_id_list(movie_id_list):
    movie_names_list = []
    movie_lengths_list = []
    movie_poster_list = []
    movie_rtr_list = []
    # getting the movie titles, lengths, posters and rotten tomato of
    # each movie id in movie_id_list
    for movie_id in movie_id_list:
        movie_name = sql("fetchone", "SELECT title FROM Movie WHERE id = ?",
                         movie_id)
        movie_names_list.append(movie_name[0])
        movie_length = sql("fetchone", "SELECT length FROM Movie WHERE id = ?",
                           movie_id)
        movie_lengths_list.append(movie_length[0])
        movie_poster = sql("fetchone",
                           "SELECT film_poster FROM Movie WHERE id = ?",
                           movie_id)
        movie_poster_list.append(movie_poster[0])
        movie_rating = sql("fetchone",
                           "SELECT audience_rating FROM Movie WHERE id = ?",
                           movie_id)
        movie_rtr_list.append(movie_rating[0])

    return [movie_names_list, movie_lengths_list,
            movie_poster_list, movie_rtr_list]


def genre_movies(genre_id_list, genre_name_list):
    # looping over a list of genre ids to find a list of ids of movies
    # in that particular genre along with their titles,
    # posters and lengths(information necessary to display
    # each movie in scrollable galleries). Information is added into the
    # dictionaries listed above under the capitalised genre names as keys
    movie_id_dict = {}
    movie_names_dict = {}
    movie_posters_dict = {}
    movie_lengths_dict = {}
    movie_rtr_dict = {}
    genre_movie_list = [movie_id_dict, movie_names_dict, movie_posters_dict,
                        movie_lengths_dict, movie_rtr_dict]
    for index, genre_id in enumerate(genre_id_list):
        genre_name = genre_name_list[index]
        movie_id_list = fetch_all_result_list("SELECT movie_id FROM "
                                              "Movie_Genre WHERE genre_id = ?",
                                              genre_id)
        movie_gallery_info = movie_gallery_info_from_movie_id_list(
            movie_id_list)
        movie_id_dict[genre_name] = movie_id_list
        movie_names_dict[genre_name] = movie_gallery_info[0]
        movie_lengths_dict[genre_name] = movie_gallery_info[1]
        movie_posters_dict[genre_name] = movie_gallery_info[2]
        movie_rtr_dict[genre_name] = movie_gallery_info[3]

    return genre_movie_list


def person_name_list_from_person_id_list(movie_people_id):
    # getting a list of people's full name from a person's id in a list of
    # people associated with a specific movie
    people_list = []
    for people in movie_people_id:
        person_id = people[1]
        first_name = sql("fetchone", "SELECT first_name FROM "
                         "People WHERE id = ?", person_id)[0]
        last_name = sql("fetchone", "SELECT last_name FROM People "
                        "WHERE id = ?", person_id)[0]
        person_name = first_name + " " + last_name
        people_list.append(person_name)

    return people_list


# ROUTES#
# homepage
@app.route("/")
def home():
    # information for genre section of home page
    genre_name_list = ["action", "drama", "comedy"]
    genre_id_list = genre_id_list_from_genre_name_list(genre_name_list)[0]
    genre_name_list = genre_id_list_from_genre_name_list(genre_name_list)[1]
    genre_movie_dict = genre_movies(genre_id_list, genre_name_list)
    # getting movies released recently in 2023
    release_year = [2022, 2023]
    final_movie_id_list = []
    final_movie_name_list = []
    final_movie_length_list = []
    final_movie_poster_list = []
    final_movie_rtr_list = []
    new_releases = [final_movie_id_list, final_movie_name_list,
                    final_movie_poster_list, final_movie_length_list,
                    final_movie_rtr_list]

    # getting the ids of movies released for each year in the
    # release_year list
    # along with their titles, posters and lengths
    # (information necessary to display each movie in scrollable galleries)
    for year in release_year:
        movie_id_list = fetch_all_result_list("SELECT id FROM Movie WHERE"
                                              " release_year = ?", year)
        movie_gallery_info = movie_gallery_info_from_movie_id_list(
            movie_id_list)
        final_movie_id_list.extend(movie_id_list)
        final_movie_name_list.extend(movie_gallery_info[0])
        final_movie_length_list.extend(movie_gallery_info[1])
        final_movie_poster_list.extend(movie_gallery_info[2])
        final_movie_rtr_list.extend(movie_gallery_info[3])

    return render_template("m_home.html", genre_movie_info=genre_movie_dict,
                           new_release_info=new_releases)


@app.route("/movie_info/<int:id>")
def movie_info(id):
    # 404 ERRORS
    # handles nonexistant urls by redirecting to 404 error page
    # Next bit of code evaluates if the movie id exists in the database.
    movie_info = sql("fetchall", "SELECT * FROM Movie WHERE id = ?", id)
    if len(movie_info) == 0:
        abort(404)
    # Next bit of code checks for rows in the Movie database where there is a
    # valid value for the id column but no valid value for the title
    # column. This means that
    # there is no substantial information about a movie
    # within the column containing a valid value for the id column
    # Thus there is no information to display and the page does not exist
    title = sql("fetchone", "SELECT title FROM Movie WHERE id = ?",
                id)[0]
    if title is None:
        abort(404)
    # MOVIE INFORMATION
    # Must retrieve information by individual columns
    # because the relative positions to each other will change
    # thus I cannot write a fetchall query and then use indexes
    # to get information from a particular column
    release_year = sql("fetchone", "SELECT release_year FROM "
                       "Movie WHERE id = ?", id)[0]
    film_poster = sql("fetchone", "SELECT film_poster FROM Movie WHERE id = ?",
                      id)[0]
    audience_rating = sql("fetchone", "SELECT audience_rating FROM Movie WHERE"
                          " id = ?", id)[0]
    length = sql("fetchone", "SELECT length FROM Movie WHERE id = ?",
                 id)[0]
    use_of_tropes_rating = sql("fetchone", "SELECT use_of_tropes_rating FROM "
                               "Movie WHERE id = ?", id)[0]
    use_of_tropes_description = sql("fetchone", "SELECT"
                                    " use_of_tropes_description FROM Movie"
                                    " WHERE id = ?", id)[0]
    moral_ambiguity_rating = sql("fetchone", "SELECT moral_ambiguity_rating"
                                 " FROM Movie WHERE id = ?", id)[0]
    moral_ambiguity_description = sql("fetchone", "SELECT"
                                      " moral_ambiguity_description FROM Movie"
                                      " WHERE id = ?", id)[0]
    description = sql("fetchone", "SELECT description FROM Movie WHERE id = ?",
                      id)[0]
    movie_info = [title, audience_rating, release_year, use_of_tropes_rating,
                  use_of_tropes_description, moral_ambiguity_rating,
                  moral_ambiguity_description, film_poster, description,
                  length]
    # getting the NZ film ratings of each movie
    # getting the description of the NZ film rating assigned to
    # the particular film so that it is clear that an R16 film is for children
    # over 16
    film_rating_id = sql("fetchone", "SELECT film_rating FROM Movie "
                         "WHERE id = ?", id)[0]
    film_rating = sql("fetchone",
                      "SELECT name FROM NZ_film_classification_rating WHERE "
                      "id = ?", film_rating_id)[0]
    film_rating_description = sql("fetchone", "SELECT description FROM "
                                  "NZ_film_classification_rating WHERE id = ?",
                                  film_rating_id)[0]
    film_rating_info = [film_rating, film_rating_description]
    # more explanation
    # Getting the names of the actors and
    # directors associated with a film
    movie_people_id = sql("fetchall",
                          "SELECT * FROM Movie_People WHERE movie_id = ?", id)
    people_list = person_name_list_from_person_id_list(movie_people_id)
    stage_name_dict = {}
    directors_list = []
    actors_list = []
    people_info = [stage_name_dict, directors_list, actors_list]
    for index, person_name in enumerate(people_list):
        person_id = movie_people_id[index][1]
        person_type_id = movie_people_id[index][2]
        # checking if the person has a stage name which could be more well
        # known to the person browsing the website
        stage_name = sql("fetchone",
                         "SELECT stage_name FROM Stage_Name WHERE id = ?",
                         person_id)
        if stage_name is not None:
            stage_name = stage_name[0]
            stage_name_dict[person_name] = stage_name
        # sorting people into actors or directors
        # making sure that those who are both
        # acting and directing in a film are in both the
        # actors_list and directors_list
        if person_type_id == 1:
            actors_list.append(person_name)
        if person_type_id == 2:
            directors_list.append(person_name)

    colour_index = id % 3
    print(colour_index)

    return render_template("m_movie_info.html", movie_info=movie_info,
                           people_info=people_info,
                           film_rating_info=film_rating_info,
                           colour_index=colour_index)


@app.route("/genre")
def genre():
    # getting information about the movies assigned to
    # to a particular genre for all the genres currently logged into my
    # database. Information to be displayed in carousels
    # First step: getting a list of all the genre ids and names in alphabetical
    # order
    genre_name_list = fetch_all_result_list("SELECT name FROM Genre", None)
    genre_id_list = genre_id_list_from_genre_name_list(genre_name_list)[0]
    genre_name_list = genre_id_list_from_genre_name_list(genre_name_list)[1]
    # Information about each genre's description is retrieved
    # To add information about each genre's description
    # to the genre_movie_list where a list of information about the movies in
    # each genre, I then appended this list of genre descriptions
    # to the genre_movie_list
    genre_descriptions = []
    for index, id in enumerate(genre_id_list):
        genre_description = sql("fetchone", "SELECT description FROM "
                                "Genre WHERE id = ?", id)
        genre_descriptions.append(genre_description[0])
    genre_movie_list = genre_movies(genre_id_list, genre_name_list)
    genre_movie_list.append(genre_descriptions)
    genre_movie_list.append(genre_name_list)

    return render_template("m_genre.html", genre_info=genre_movie_list)


@app.route("/cinema_eras")
def cinema_eras():
    # getting the information about movies needed for display in
    # galleries (their title, poster, rotten tomatoes rating, length)
    # and separating based on eras of tilm
    # Golden Age of Hollywood: all films made up until 1960
    # New Age of Hollywood: 1961 to 1975
    # Blockbuster Age of Hollywood: all films made after 1975
    golden_age_of_hollywood = []
    new_age_of_hollywood = []
    blockbuster_age_of_hollywood = []
    cinema_eras_dict = {"Golden Age Of Hollywood": golden_age_of_hollywood,
                        "New Age Of Hollywood": new_age_of_hollywood,
                        "Blockbuster Age Of Hollywood":
                        blockbuster_age_of_hollywood}
    for key in cinema_eras_dict:
        if key == "Golden Age Of Hollywood":
            movie_id_list = fetch_all_result_list("SELECT id FROM Movie WHERE "
                                                  "release_year <= 1960", None)
        elif key == "New Age Of Hollywood":
            movie_id_list = fetch_all_result_list("SELECT id FROM Movie WHERE "
                                                  "release_year > 1960 and "
                                                  "release_year <= 1975", None)
        elif key == "Blockbuster Age Of Hollywood":
            movie_id_list = fetch_all_result_list("SELECT id FROM Movie WHERE "
                                                  "release_year > 1975", None)
        cinema_eras_dict[key] = movie_gallery_info_from_movie_id_list(
            movie_id_list)
        cinema_eras_dict[key].append(movie_id_list)

    return render_template("m_cinema_eras.html",
                           cinema_eras_dict=cinema_eras_dict)


@app.route("/rotten_tomatoes")
def rotten_tomatoes():
    # getting the information about movies needed for display in
    # galleries (their title, poster, rotten tomatoes rating, length)
    # and separating based on each rotten tomato score of tilm
    # Great Score: rotten tomato rating above 75
    # Good Score: rotten tomato rating between 60 and 75
    # Bad Score: rotten tomato rating below 60
    great_score = []
    good_score = []
    bad_score = []
    rtr_dict = {"Great Score": great_score,
                "Good Score": good_score,
                "Bad Score": bad_score}
    for key in rtr_dict:
        if key == "Great Score":
            movie_id_list = fetch_all_result_list("SELECT id FROM Movie "
                                                  "WHERE audience_rating >= "
                                                  "75", None)
        elif key == "Good Score":
            movie_id_list = fetch_all_result_list("SELECT id FROM Movie "
                                                  "WHERE audience_rating < 75 "
                                                  "AND audience_rating >= 60",
                                                  None)
        elif key == "Bad Score":
            movie_id_list = fetch_all_result_list("SELECT id FROM Movie "
                                                  "WHERE audience_rating < 60",
                                                  None)
        rtr_dict[key] = movie_gallery_info_from_movie_id_list(
            movie_id_list)
        rtr_dict[key].append(movie_id_list)

    return render_template("m_rotten_tomatoes.html",
                           rotten_tomatoes_dict=rtr_dict)


@app.errorhandler(404)
def error(e):
    return render_template("error404.html")


if __name__ == "__main__":
    app.run(debug=True)
