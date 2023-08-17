import sqlite3

#genre_name = input("genre_name: ").title()
#genre_id = cursor.execute("SELECT id FROM Genre WHERE name = ?",(genre_name,)).fetchone()
#t = type(genre_id[0])
#print(t)
#if genre_id == None:
    #print("genre_name is invalid")
#else:
    #genre_id = genre_id[0]
    #print(genre_id)

#genre_name = input("genre_name: ").title()
#genre_id = cursor.execute("SELECT id FROM Genre WHERE name = ?",(genre_name,)).fetchone()
#genre_id = genre_id[0]

#query_i = "SELECT id FROM Movie WHERE film_rating IN (5,6)"
#query_ii = "SELECT id FROM Movie WHERE release_year >= 2000"
#Query = query_i + 'UNION ' + query_ii
#result = cursor.execute(Query).fetchall()
#print(result)


#film_query_result = []
#release_year_result = []
#movie_length_result = []
#film_rating_query = cursor.execute("SELECT id FROM Movie WHERE film_rating IN (5,6)").fetchall()
#release_year_query = cursor.execute("SELECT id FROM Movie WHERE release_year >= 2000").fetchall()
#movie_length_query = cursor.execute("SELECT id FROM Movie WHERE length > 90").fetchall()

#for item in range(len(film_rating_query)):
    #film_query_result.append(film_rating_query[item][0])
#for item in range(len(release_year_query)):
    #release_year_result.append(release_year_query[item][0])
#for item in range(len(movie_length_query)):
    #movie_length_result.append(movie_length_query[item][0])

#film_rating_set = set(film_query_result)
#release_year_set = set(release_year_result)
#movie_length_set = set(movie_length_result)

#new_list = list(film_rating_set.intersection(release_year_result,movie_length_set))

#print(new_list)

def sql(fetch_status,query,constraint):
    conn = sqlite3.connect("Movie_Database_1.db")
    cur = conn.cursor()
    if fetch_status == "fetchone":
        fetch_result = cur.execute(query,(constraint,)).fetchone()
    if fetch_status == "fetchall":
        fetch_result = cur.execute(query,(constraint,)).fetchall()
    return fetch_result

def another_funct():
    genre_list =  ["horror","romance","martial arts","comedy","drama","Science Fiction"]
    genre_id_list = []
    for genre_name in genre_list:
        genre_name_db = genre_name.title()
        genre_id = sql("fetchone","SELECT id FROM Genre WHERE name = ?",genre_name_db)
        genre_id_list.append(genre_id[0])
    print(genre_id_list)

another_funct()

