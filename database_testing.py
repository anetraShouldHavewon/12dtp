import sqlite3
conn = sqlite3.connect("Movie_Database_1.db")
cursor = conn.cursor()

genre_name = input("genre_name: ").title()
genre_id = cursor.execute("SELECT id FROM Genre WHERE name = ?",(genre_name,)).fetchone()
if genre_id == None:
    print("genre_name is invalid")
else:
    genre_id = genre_id[0]
    print(genre_id)

genre_name = input("genre_name: ").title()
genre_id = cursor.execute("SELECT id FROM Genre WHERE name = ?",(genre_name,)).fetchone()
genre_id = genre_id[0]

