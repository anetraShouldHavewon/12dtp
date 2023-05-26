import sqlite3
conn = sqlite3.connect("Movie_Database_1.db")
cursor = conn.cursor()

for id in range(1,5):
    genre_id = cursor.execute("SELECT genre_id FROM Movie_Genre WHERE movie_id = ?", (id,)).fetchall()
    print(genre_id)
    
    li_genre_id = []
