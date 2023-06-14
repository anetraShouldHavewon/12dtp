from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

#homepage
@app.route("/home")
def home():
    conn = sqlite3.connect("Movie_Database_1.db")
    cur = conn.cursor()
    
    #functions#
    #getting a list of agenre ids from a list of names of genres
    def genre_id_from_genre_name(genre_list):
        genre_id_list = []
        for genre_name in genre_list:
            genre_name = genre_name.title()
            genre_id = cur.execute("SELECT id FROM Genre WHERE name = ?",(genre_name,)).fetchone()
            if genre_id == None:
                print("genre_name is invalid")  #test print line
                genre_list.remove(genre_name)
            else:
                genre_id = genre_id[0]
                genre_id_list.append(genre_id)

        genre_dict = {
            "genre_list" : genre_list,
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
    genre_list =  ["romance", "horor"]
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

#@app.route("/movie_info/<int:id>")
#def movie_info(id):

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