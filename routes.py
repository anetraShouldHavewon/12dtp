from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

#homepage
@app.route("/home")
def home():
    conn = sqlite3.connect("Movie_Database_1.db")
    cur = conn.cursor()
    
    #functions/queries#
    #getting a list of agenre ids from a list of names of genres
    def genre_id_from_genre_name(genre_list):
        genre_id_list = []
        new_genre_list = []

        for genre_name in genre_list:
            print(genre_name)
            genre_name_db = genre_name.title()
            genre_id = cur.execute("SELECT id FROM Genre WHERE name = ?",(genre_name_db,)).fetchone()
            if genre_id == None:
                print("{} is invalid".format(genre_name_db))  #test print line
            else:
                print("{} is valid".format(genre_name_db))  #test print line
                new_genre_list.append(genre_name_db)
                genre_id = genre_id[0]
                genre_id_list.append(genre_id)


        genre_dict = {
            "genre_list" : new_genre_list,
            "genre_id_list": genre_id_list, 
        }  

        return genre_dict
          
    #getting a list of movie ids and their namesfrom a list of genre ids
    #getting movie_ids from a genre_id
    def movie_id_from_genre_id(genre_id):
        movie_id_list = []
        movie_ids = cur.execute("SELECT movie_id FROM Movie_Genre WHERE genre_id = ?",(genre_id,)).fetchall()
        for movie_id in range(len(movie_ids)):
            movie_id_list.append(movie_ids[movie_id][0])
        return movie_id_list

    #getting movie names from movie_ids
    def movie_name_from_genre_id(movie_id_list):
        movie_names_list = []
        for movie_id in movie_id_list:
            movie_name = cur.execute("SELECT title FROM Movie WHERE id = ?",(movie_id,)).fetchone()
            movie_names_list.append(movie_name[0])
        return movie_names_list
    
    #variables
    genre_list =  ["horror","romance","martial arts","comedy","drama","Science Fiction"]
    genre_id_list = genre_id_from_genre_name(genre_list)["genre_id_list"]
    genre_list = genre_id_from_genre_name(genre_list)["genre_list"]

    movie_id_dict = {}
    movie_names_dict = {}

    for id in range(len(genre_id_list)):
        genre_id = genre_id_list[id]
        movie_id_list = movie_id_from_genre_id(genre_id)
        movie_id_dict[genre_list[id]] = movie_id_list
        movie_name_list = movie_name_from_genre_id(movie_id_list)
        movie_names_dict[genre_list[id]] = movie_name_list

    return render_template("home.html", genre_ids = genre_id_list, movie_ids = movie_id_dict, movie_names = movie_names_dict)

@app.route("/movie_info/<int:id>")
def movie_info(id):
    conn = sqlite3.connect("Movie_Database_1.db")
    cur = conn.cursor()
    
    #functions#
    def person_name_list_from_person_id_list(movie_people_id):
        people_list = []
        for people in movie_people_id:
            person_id = people[0]
            person_first_name = cur.execute("SELECT first_name FROM People WHERE id = ?",(person_id,)).fetchone()[0]
            person_last_name = cur.execute("SELECT last_name FROM People WHERE id = ?",(person_id,)).fetchone()[0]
            person_name = person_first_name + " " + person_last_name
            people_list.append(person_name)

        return people_list
        
    def stage_name_from_person_id(person_id):
        stage_name = cur.execute("SELECT stage_name FROM Stage_Name WHERE id = ?",(person_id,)).fetchone()
        if stage_name != None:
            stage_name = stage_name[0]

            return stage_name

    #queries#
    movie_info = cur.execute("SELECT * FROM Movie WHERE id = ?",(id,)).fetchone()
    movie_people_id = cur.execute("SELECT * FROM Movie_People WHERE movie_id = ?", (id,)).fetchall()
    
    #variables#
    #people-info#
    stage_name_dict = {}
    directors_list = []
    actors_list = []

    people_list = person_name_list_from_person_id_list(movie_people_id)
    for person in people_list:
        person_name = person
        person_id = movie_people_id[people_list.index(person)][1]
        person_type_id = movie_people_id[people_list.index(person)][2]

        stage_name = stage_name_from_person_id(person_id)
        stage_name_dict[person_name] = stage_name
        
        if person_type_id == 1:
            actors_list.append(person_name)
        elif person_type_id == 2: 
            directors_list.append(person_name)

    return render_template("movie_info.html", movie_info = movie_info, people_list = people_list, stage_names = stage_name_dict, directors_list = directors_list, actors_list = actors_list)


@app.route("/explore")
def explore():
    conn = sqlite3.connect("Movie_Database_1.db")
    cur = conn.cursor()
    
    #functions/queries#
    #getting a list of genre ids from a list of names of genres
    def genre_id_from_genre_name(genre_list):
        genre_id_list = []
        new_genre_list = []

        for genre_name in genre_list:
            print(genre_name)
            genre_name_db = genre_name.title()
            genre_id = cur.execute("SELECT id FROM Genre WHERE name = ?",(genre_name_db,)).fetchone()
            if genre_id == None:
                print("{} is invalid".format(genre_name_db))  #test print line
            else:
                print("{} is valid".format(genre_name_db))  #test print line
                new_genre_list.append(genre_name_db)
                genre_id = genre_id[0]
                genre_id_list.append(genre_id)


        genre_dict = {
            "genre_list" : new_genre_list,
            "genre_id_list": genre_id_list, 
        }  

        return genre_dict

    #getting a list of movie ids and their names from a list of genre ids
    #getting movie_ids from a genre_id
    def movie_id_from_genre_id(genre_id):
        movie_id_list = []
        movie_ids = cur.execute("SELECT movie_id FROM Movie_Genre WHERE genre_id = ?",(genre_id,)).fetchall()
        for movie_id in range(len(movie_ids)):
            movie_id_list.append(movie_ids[movie_id][0])
        return movie_id_list

    #getting movie names from movie_ids
    def movie_name_from_movie_id(movie_id_list):
        movie_names_list = []
        for movie_id in movie_id_list:
            movie_name = cur.execute("SELECT title FROM Movie WHERE id = ?",(movie_id,)).fetchone()
            movie_names_list.append(movie_name[0])
        return movie_names_list

    #getting a list of movie ids based on their release year
    def movie_ids_from_release_year(release_year):
        movie_id_list = []
        movie_ids = cur.execute("SELECT id FROM Movie WHERE release_year = ?",(release_year,)).fetchall()
        for id in movie_ids:
            movie_id_list.append(id[0])
        return movie_id_list
    
    #variables
    #getting movies and their info based on the genre
    genre_list =  ["horror","romance","martial arts","comedy","drama","Science Fiction"]
    genre_id_list = genre_id_from_genre_name(genre_list)["genre_id_list"]
    genre_list = genre_id_from_genre_name(genre_list)["genre_list"]

    movie_id_dict = {}
    movie_names_dict = {}
    genre_descriptions = {}
    genre_movie_ids = {}
    
    for id in range(len(genre_id_list)):
        genre_id = genre_id_list[id]
        genre_name = genre_list[id]
        genre_description = cur.execute("SELECT description FROM Genre WHERE id = ?",(genre_id,))
        genre_descriptions[genre_name] = genre_description
        movie_id_list = movie_id_from_genre_id(genre_id)
        movie_id_dict[genre_name] = movie_id_list
        movie_name_list = movie_name_from_movie_id(movie_id_list)
        movie_names_dict[genre_name] = movie_name_list
        #getting rotten tomatoes rating of each movie
        one_genre_movies_rtr = {}
        for movie_id in movie_id_list:
            rtr = cur.execute("SELECT audience_rating FROM Movie WHERE id = ?",(movie_id,))
            index = movie_id_list.index(movie_id)
            one_genre_movies_rtr[movie_name_list[index]] = rtr
        genre_movie_ids[genre_name] = one_genre_movies_rtr

    #getting movies released recently(in 2022 or 2023)
    release_year = [2022,2023]
    two_zero_two_two_movies = {}
    two_zero_two_three_movies = {}
    list_of_year_dicts = [two_zero_two_two_movies, two_zero_two_three_movies]

    for year in release_year:
        index = release_year.index(year)
        year_dict = list_of_year_dicts[index]
        movie_id_list = movie_ids_from_release_year(year)
        year_dict["movie_id_list"] = movie_id_list
        movie_name_list = movie_name_from_movie_id(movie_id_list)
        year_dict["movie_name_list"] = movie_name_list
        movie_rtr = {}
        movie_poster = {}
        for name in movie_name_list:
            rtr = cur.execute("SELECT audience_rating FROM Movie WHERE name = ?",(name,))
            movie_rtr[name] = rtr
            poster = cur.execute("SELECT film_poster FROM Movie WHERE name = ?", (name,))
            movie_poster[name] = poster

        year_dict = {
            "movie_id_list": movie_id_list,
            "movie_name_list" : movie_name_list,
            "movie ratings": movie_rtr,
            "movie_posters": movie_poster
        }

    return render_template("explore.html", genre_ids = genre_id_list, movie_ids = movie_id_dict, movie_names = movie_names_dict, genre_descriptions = genre_descriptions, two_zero_two_two_movies = two_zero_two_two_movies, two_zero_two_three_movies = two_zero_two_three_movies)

    
#@app.route("/quiz_question/<int:question_num")
#def quiz_question(question_num):

#@app.route("/quiz_results")
#def quiz_results():

#@app.route("/my_watchlist")
#def my_watchlist():

#@app.route("/to_watch_list")
#def to_watch_list():

#@app.route("/watched_list")
#def watched_list():

if __name__ == "__main__":
    app.run(debug = True)