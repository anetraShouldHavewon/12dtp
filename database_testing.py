import sqlite3

connection = sqlite3.connect("Movie_Database_1.db")
cursor = connection.cursor()
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

def sql(fetch_status,
        queryiiiii, constraint):
    conn = sqlite3.connect("Movie_Database_1.db")
    cur = conn.cursor()
    if constraint is None:
        if fetch_status == "fetchone":
            fetch_result = cur.execute(queryiiiii).fetchone()
        if fetch_status == "fetchall":
            fetch_result = cur.execute(queryiiiii).fetchall()
    else:
        if fetch_status == "fetchone":
            fetch_result = cur.execute(queryiiiii,
                                       (constraint,)).fetchone()
        if fetch_status == "fetchall":
            fetch_result = cur.execute(queryiiiii,
                                       (constraint,)).fetchall()
    return fetch_result

def gallery_img_info_from_movie_list(movie_list,movie_dict):
    poster_dict = {}
    length_dict = {}
    rtr_dict = {}

    for movie in movie_list:
        poster = sql("fetchone", "SELECT film_poster FROM Movie WHERE title = ?", movie)[0]
        poster_dict[movie] = poster
        length = sql("fetchone","SELECT length FROM Movie WHERE title = ?",movie)[0]
        length_dict[movie] = length
        rtr = sql("fetchone","SELECT audience_rating FROM Movie WHERE title = ?", movie)[0]
        rtr_dict[movie] = rtr
        
    movie_dict["movies"] = movie_list
    movie_dict["posters"] = poster_dict
    movie_dict["lengths"] = length_dict
    movie_dict["rtrs"] = rtr_dict

    return movie_dict

great_score = {}
good_score = {}
bad_score = {}

rtr_list = [great_score, good_score, bad_score]

rtr_dict = {"Great Score": great_score,
                "Good Score": good_score,
                "Bad Score": bad_score}
    
for score_range in rtr_list:
    if score_range == great_score:
        movies = sql(
            "fetchall", "SELECT title FROM Movie WHERE audience_rating >= 75",
            None)
        #(movies)
    #elif score_range == good_score:
        #movies = sql("fetchall","SELECT title FROM Movie WHERE film_rating < 75 AND film_rating >= 60", None)
    #elif score_range == bad_score:
        #movies = sql("fetchall","SELECT title FROM Movie WHERE film_rating < 60", None)

    movie_list = []
    for movie in movies:
        movie_list.append(movie[0])

    score_range = gallery_img_info_from_movie_list(
        movie_list, score_range)
        
#print(
    #rtr_dict["Great Score"])

title = sql("fetchone", "SELECT title FROM Movie WHERE id = ?",1)
film_rating_id = sql("fetchone", "SELECT film_rating FROM Movie WHERE id = ?", 1)[0]
print(title)

