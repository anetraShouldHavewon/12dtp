from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route("/home")
def home():

@app.route("/movie_info/<int:id>")
def movie_info(id):

@app.route("/explore")
def explore():

@app.route("/quiz_question/<int:question_num")
def quiz_question(question_num):

@app.route("/quiz_results")
def quiz_results():

@app.route("/my_watchlist")
def my_watchlist():

@app.route("/to_watch_list")
def to_watch_list():

@app.route("/watched_list")
def watched_list():

if __name__ == "__main__":
    app.run(debug = True)