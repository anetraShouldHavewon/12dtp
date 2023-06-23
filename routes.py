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
    def person_name_stage_name_from_person_id(movie_people):
        people_list = []
        for people in movie_people:
            person_id = people[0]
            person_first_name = cur.execute("SELECT first_name FROM People WHERE id = ?",(person_id,)).fetchone()[0]
            person_last_name = cur.execute("SELECT last_name FROM People WHERE id = ?",(person_id,)).fetchone()[0]
            person_name = person_first_name + " " + person_last_name
            people_list.append(person_name)

        return people_list
        
    def stage_name_from_person_id(person_name, person_id):
        stage_name = cur.execute("SELECT stage_name FROM Stage_Name WHERE id = ?",(person_id,)).fetchone()
        if stage_name != None:
            stage_name = stage_name[0]

            stage_name_dict = {
                person_name: stage_name
            }
            return stage_name_dict
        
    def type_of_person_from_person_id(movie_people):
        for person in movie_people:
            person_type_id = person[2]
            person_type = cur.execute("SELECT name FROM Type_of_Person WHERE id = ?",(person_type_id,)).fetchone()[0]
            return person_type

    #queries#
    movie_info = cur.execute("SELECT * FROM Movie WHERE id = ?",(id,)).fetchone()
    movie_people = cur.execute("SELECT * FROM Movie_People WHERE movie_id = ?", (id,)).fetchall()
    people_list = person_name_stage_name_from_person_id(movie_people)
    for person in people_list:
        

    #variables#
    title = movie_info[1]
    release_year = movie_info[2]
    audience_ratings = movie_info[3]
    use_of_tropes_rating = movie_info[4]
    use_of_tropes_description = movie_info[5]
    moral_ambiguity_rating = movie_info[6]
    moral_ambiguity_description = movie_info[7]
    film_rating = movie_info[8]
    length = movie_info[9]
    poster = movie_info[10]
    
    def stage_name_from_person_id(people_list, movie_people):
        stage_name_dict = {}
        for people in people_list:
            index = people_list.index(people)
            person_id = movie_people[index][0]
            stage_name = cur.execute("SELECT stage_name FROM Stage_Name WHERE id = ?",(person_id,)).fetchone()
            if stage_name != None:
                stage_name = stage_name[0]


    return render_template("movie_info.html",movie_info = movie_info)


#@app.route("/explore")
#def explore():

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