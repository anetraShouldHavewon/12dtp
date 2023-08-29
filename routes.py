from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

#opening connection to sql database, evaluating if the query used is a fetchone or fetchall and returning the result of the query
#this function deals with getting data from the "Movie_Database_1.db"
def sql(fetch_status,query,constraint):
    conn = sqlite3.connect("Movie_Database_1.db")
    cur = conn.cursor()
    if constraint == None:
        if fetch_status == "fetchone":
            fetch_result = cur.execute(query).fetchone()
        if fetch_status == "fetchall":
            fetch_result = cur.execute(query).fetchall()
    else:
        if fetch_status == "fetchone":
            fetch_result = cur.execute(query,(constraint,)).fetchone()
        if fetch_status == "fetchall":
            fetch_result = cur.execute(query,(constraint,)).fetchall()

    return fetch_result

#ALL FUNCTIONS BEYOND THIS POINT TAKE DATA TAKEN FROM DATABASES AND PUTS THEM INTO MANAGEABLE LIST FORMS#
#getting a list of ids of genres in a list of genres names
def genre_id_list_from_genre_name_list(genre_list):
    genre_id_list = []
    genre_list.sort()
    new_genre_list = []

    for genre_name in genre_list:
        #retrieving data from database
        genre_name_db = genre_name.title()
        genre_id = sql("fetchone","SELECT id FROM Genre WHERE name = ?",genre_name_db)

        #evaluating if there genre_id is a valid result
        #if genre_id does not exist, the genre name in the list of genres is misspelt or does not exist in the database yet
        if genre_id == None:
            print("{} is invalid.\nMaybe the genre name is misspelt or this genre does not yet exist in the database yet.".format(genre_name_db))  #testing error line
        else:
            genre_id = genre_id[0]
            genre_id_list.append(genre_id)
        new_genre_list.append(genre_name_db)

    return [genre_id_list,new_genre_list]

#getting a list of ids of movies of a particular genre using the genre's id
def movie_id_from_genre_id(genre_id):
    movie_id_list = []
    movie_ids = sql("fetchall","SELECT movie_id FROM Movie_Genre WHERE genre_id = ?",genre_id)
    for movie_id in range(len(movie_ids)):
        movie_id_list.append(movie_ids[movie_id][0])
    return movie_id_list

#getting the movie titles of a movie id in a list
def movie_name_from_movie_id_list(movie_id_list):
    movie_names_list = []
    for movie_id in movie_id_list:
        movie_name = sql("fetchone","SELECT title FROM Movie WHERE id = ?",movie_id)
        movie_names_list.append(movie_name[0])
    return movie_names_list

#getting the movie poster of a movie id in a list
def movie_posters_list_from_movie_id_list(movie_id_list):
    movie_poster_list = []
    for movie_id in movie_id_list:
        movie_poster = sql("fetchone","SELECT film_poster FROM Movie WHERE id =?",movie_id)
        movie_poster_list.append(movie_poster[0])
    return movie_poster_list

#getting a person's name from a person's id from a list
def person_name_list_from_person_id_list(movie_people_id):
    people_list = []
    for people in movie_people_id:
        person_id = people[1]
        person_first_name = sql("fetchone","SELECT first_name FROM People WHERE id = ?",person_id)[0]
        person_last_name = sql("fetchone","SELECT last_name FROM People WHERE id = ?",person_id)[0]
        person_name = person_first_name + " " + person_last_name
        people_list.append(person_name)

    return people_list

#getting a person's stage name from a person's name     
def stage_name_from_person_id(person_id):
    stage_name = sql("fetchone","SELECT stage_name FROM Stage_Name WHERE id = ?",person_id)
    if stage_name != None:
        stage_name = stage_name[0]

    return stage_name


#getting a list of movie ids based on their release year
def movie_ids_from_release_year(release_year):
    movie_id_list = []
    movie_ids = sql("fetchall","SELECT id FROM Movie WHERE release_year = ?",release_year)
    for movie_id in movie_ids:
        movie_id_list.append(movie_id[0])

    return movie_id_list
    
#ROUTES#

#homepage
@app.route("/home")
def home():
    #genres
    genre_list =  ["action","drama","comedy"]
    genre_id_list = genre_id_list_from_genre_name_list(genre_list)[0]
    genre_list = genre_id_list_from_genre_name_list(genre_list)[1]

    #movies of certain genres
    movie_id_dict = {}
    movie_names_dict = {}
    movie_posters_dict = {}

    for id in range(len(genre_id_list)):
        genre_id = genre_id_list[id]
        movie_id_list = movie_id_from_genre_id(genre_id)
        movie_id_dict[genre_list[id]] = movie_id_list
        movie_name_list = movie_name_from_movie_id_list(movie_id_list)
        movie_names_dict[genre_list[id]] = movie_name_list
        movie_posters_list = movie_posters_list_from_movie_id_list(movie_id_list)
        movie_posters_dict[genre_list[id]] = movie_posters_list

    return render_template("m_home.html", genre_list = genre_list, genre_ids = genre_id_list, movie_ids = movie_id_dict, movie_names = movie_names_dict, movie_posters = movie_posters_dict)

@app.route("/movie_info/<int:id>")
def movie_info(id):
    #movie-info#
    movie_info = sql("fetchone","SELECT * FROM Movie WHERE id = ?",id)
    movie_people_id = sql("fetchall","SELECT * FROM Movie_People WHERE movie_id = ?",id)

    #film-rating
    film_rating_id = movie_info[3]
    film_rating = sql("fetchone","SELECT name FROM NZ_film_classification_rating WHERE id = ?",film_rating_id)
    film_rating_description = sql("fetchone","SELECT description FROM NZ_film_classification_rating WHERE id = ?",film_rating_id)

    #people-info#
    people_list = person_name_list_from_person_id_list(movie_people_id)
    stage_name_dict = {}
    directors_list = []
    actors_list = []

    for person in people_list:
        person_name = person
        person_id = movie_people_id[people_list.index(person)][1]
        person_type_id = movie_people_id[people_list.index(person)][2]

        stage_name = stage_name_from_person_id(person_id)
        if stage_name != None:
            stage_name_dict[person_name] = stage_name
        
        if person_type_id == 1:
            actors_list.append(person_name)
        elif person_type_id == 2: 
            directors_list.append(person_name)

    return render_template("m_movie_info.html", movie_info = movie_info, people_list = people_list, stage_names = stage_name_dict, directors_list = directors_list, actors_list = actors_list, film_rating = film_rating, film_rating_description = film_rating_description)


@app.route("/explore")
def explore():
    #getting movies and their info based on the genre
    genre_list =  []
    genres = sql("fetchall","SELECT name FROM Genre",None)
    for genre in genres:
        genre_list.append(genre[0])
    genre_id_list = genre_id_list_from_genre_name_list(genre_list)[0]
    genre_list = genre_id_list_from_genre_name_list(genre_list)[1]

    movie_names_dict = {}
    genre_descriptions = {}
    genre_movie_rtr = {}
    movie_id_dict = {}

    for id in range(len(genre_id_list)):
        genre_id = genre_id_list[id]
        genre_name = genre_list[id]
        genre_description = sql("fetchone","SELECT description FROM Genre WHERE id = ?",genre_id)
        genre_descriptions[genre_name] = genre_description[0]
        movie_id_list = movie_id_from_genre_id(genre_id)
        movie_name_list = movie_name_from_movie_id_list(movie_id_list)
        movie_names_dict[genre_name] = movie_name_list
        movie_id_dict[genre_name] = movie_id_list

        #getting rotten tomatoes rating of each movie
        genre_movie_rtr_list = []
        for movie_id in movie_id_list:
            rtr = sql("fetchone","SELECT audience_rating FROM Movie WHERE id = ?",movie_id)
            index = movie_id_list.index(movie_id)
            genre_movie_rtr_list.append(rtr[0])
        genre_movie_rtr[genre_name] = genre_movie_rtr_list
    
    print(movie_id_dict)
    #getting movies released recently(in 2022 or 2023)
    release_year = [2023]
    two_zero_two_three_movies = {}
    list_of_year_dicts = [two_zero_two_three_movies]

    for year in release_year:
        index = release_year.index(year)
        year_dict = list_of_year_dicts[index]
        movie_id_list = movie_ids_from_release_year(year)
        movie_name_list = movie_name_from_movie_id_list(movie_id_list)

        movie_rtr = {}
        movie_poster = {}
        movie_id = {}

        for name in movie_name_list:
            rtr = sql("fetchone","SELECT audience_rating FROM Movie WHERE title = ?",name)
            movie_rtr[name] = rtr[0]
            poster = sql("fetchone","SELECT film_poster FROM Movie WHERE title = ?",name)
            movie_poster[name] = poster[0]
            movie_id[name] = movie_id_list[movie_name_list.index(name)]

        year_dict["movie_ids"] = movie_id
        year_dict["movie_ratings"] = movie_rtr
        year_dict["movie_posters"] = movie_poster
      

    return render_template("m_explore.html", genre_list = genre_list, genre_descriptions = genre_descriptions, movie_ids = movie_id_dict, movie_names = movie_names_dict, genre_movie_rtr = genre_movie_rtr, two_zero_two_three_movies = two_zero_two_three_movies)

        
#passing flask object to javascript
if __name__ == "__main__":
    app.run(debug = True)