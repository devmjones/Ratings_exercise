from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2

app = Flask(__name__)
app.secret_key = "ShutUp"
app.jinja_env.undefined = jinja2.StrictUndefined



@app.route("/sign_up")
def index():
    user_list = model.session.query(model.User).limit(5).all()
    return render_template("index.html", user_list = user_list)

@app.route("/signup", methods=["GET"])
def show_signup():
    return render_template("sign_up.html")

@app.route("/signup", methods=["POST"])
def process_signup():
    email = request.form['email']
    password = request.form['password']
    age = request.form['age']
    zipcode = request.form['zipcode']

    #making a new instances of the User class called 'user'
    user = model.User(email=email, password=password, age=age, zipcode=zipcode)
    model.session.add(user) #adding to database session
    model.session.commit() #saving into database
    #id_search = model.session.query(model.User).filter_by(email=email).one()
   
   # user_id= id_search.id

    # we would like this to
    # - show user profile page
    # - on user profile page will be :
    # --- link to list of users
    # --- movies they've rated (with option to rerate)
    # --- link to rate more movies
    #"/users/949"
    flash("You have successfully been added to our judgemental database! Please click on a movie to rate")
    return redirect ("/movies")
    #return redirect ("/users/%s" % user_id) 

@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def process_login():
#     """user enters email ,used to look up in DB."""
    email = request.form['email']
    password = request.form['password']
#     """setting variable user object equal to result from sqlalchemy query"""
    user = model.session.query(model.User).filter_by(email=email).filter_by(password=password).first()
    user_id= user.id
    if user:
        session["email"] = user
        flash("Login successful")
        print session
        if len(user.ratings) == 0:
            flash("You haven't rated any movies. Please click on a movie to rate.")
            return redirect("/movies")
        else:
            return redirect ("/users/%s" % user_id)    
    else:
        flash("You typed something wrong. Try again")
        print session
        return redirect("/login")

@app.route("/users")
def show_users():
    user_list = model.session.query(model.User).all()
    return render_template("user_list.html", user_list = user_list)

@app.route("/users/<int:id>") 
def show_user_details(id): 
    user = model.session.query(model.User).filter_by(id=id).first()
    print "*****************************", user.id
   
    ratings_list = user.ratings
    print ratings_list
    print ratings_list[0].movie.name #this gives the name of the first movie in the user's ratings
    num_ratings = len(ratings_list)

    return render_template("user_details.html", ratings_list=ratings_list, user=user, num_ratings=num_ratings)

@app.route("/movies")
def show_movies():
    movie_list = model.session.query(model.Movie).all()
    return render_template("movie_list.html", movie_list = movie_list)


@app.route("/movies/<int:id>") 
def show_movie_details(id): 
    movie = model.session.query(model.Movie).filter_by(id=id).first()
    print "*****************************", movie.id
   
    ratings_list = movie.ratings
    print ratings_list
    print ratings_list[0].user.id #this gives the name of the user who has the first rating
    num_ratings = len(ratings_list)

    return render_template("movie_details.html", ratings_list=ratings_list, movie=movie, num_ratings=num_ratings)



if __name__ == "__main__":
    app.run(debug = True)