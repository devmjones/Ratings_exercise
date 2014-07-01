import model
import csv
import datetime

def load_users(session):
    # use u.user
    user_file = open("seed_data/u.user")
    for line in user_file:
        line = line.rstrip()
        user_data = line.split('|')
        #line 12 assigns the variable "user", to the class User in the file model.py
        user = model.User(id=user_data[0],
            age=user_data[1],
            zipcode=user_data[4])
    
        session.add(user)
    
    session.commit()    

    return True

def load_movies(session):
    movie_file = open("seed_data/u.item")
    for line in movie_file:
        line = line.rstrip()

        movie_data = line.split('|')

        movie_title = movie_data[1]
        #line 31 takes the last 6 char off the title, to remove the release date.
        movie_title = movie_title[:-6]
        #line 33 compensates for any latin flavor our titles may have
        movie_title = movie_title.decode("latin-1")
        #line 35 states that if our relased_at is an empty string, fill it with some crap
        if movie_data[2] == "":
            movie_data[2] = "01-Jan-1900"
        #line 38 converts the datetime string into a datetime object
        convert_date = datetime.datetime.strptime(movie_data[2],"%d-%b-%Y")
       
        movie = model.Movie(id= movie_data[0],
            name=movie_title, 
            released_at=convert_date, 
            imdb_url= movie_data[4])

        session.add(movie)
    session.commit()   
        
    return True

def load_ratings(session):
    ratings_file = open("seed_data/u.data")
    # line 53 creates an artifical primary key, since there isn't one in the file
    counter = 1
    for line in ratings_file:
        line = line.rstrip()
        ratings_data = line.split()
        rating = model.Rating(id = counter,
            user_id = ratings_data[0],
            movie_id = ratings_data[1],
            rating = ratings_data[2])
        counter += 1
        # print rating.id, rating.user_id, rating.movie_id, rating.rating

        session.add(rating)
    
    session.commit()    

    return True

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    # these functions 'seed' the database ratings.db
    # load_users(session)
    # load_movies(session)
    # load_ratings(session)    

if __name__ == "__main__":
    s= model.connect()
    main(s)
