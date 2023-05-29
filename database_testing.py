import sqlite3
conn = sqlite3.connect("Movie_Database_1.db")
cursor = conn.cursor()

#GETTING MOVIE ID FROM ITS NAME#
#movie_name = str.title(input("movie name: "))
#while movie_name not in [" ",""]:
    #movie_id = cursor.execute("SELECT id FROM Movie WHERE title = ?",(movie_name,)).fetchone()
    #print(movie_id)
    #movie_name = str.title(input("movie name: "))
#else:
    #print("See you")

movie_id = input("movie id?: ")
if movie_id.isdigit():
    genre_ids = cursor.execute("SELECT genre_id FROM Movie_Genre WHERE movie_id = ?", (movie_id,)).fetchall()
    print(genre_ids)
else:
    print("movie id not valid")

genre_list = []
for genre_id in genre_ids:
    genre_list.append(genre_id[0])
print(genre_list)

