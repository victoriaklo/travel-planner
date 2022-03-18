"""Server for travel and planning app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, db
import crud
import requests
import os

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "key"
app.jinja_env.undefined = StrictUndefined

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


API_KEY = os.environ['GOOGLEMAPS_KEY']

### ---------------- ROUTES FOR HOME/LOGIN --------------- ###


@app.route("/")
def homepage():
    """View homepage."""

    user_id = session.get('user_email')
    if user_id:
        return redirect('/login')

    return render_template("login.html")


@app.route("/register", methods=["POST"])
def register_user():
    """Create a new user."""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(first_name, last_name, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")



@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        return redirect("/")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        return redirect("/main")


@app.route("/main")
def render_main_page():
    """Renders main page"""
    return render_template("main.html")



### ---------------- ROUTES FOR MAIN/GLOBE PAGE --------------- ###


### ---------------- ROUTES FOR USER PROFILE PAGE --------------- ###
# @app.route("/user_profile")
# def display_profile():
#     """Displays the user profile"""
#     user = crud.get_user_by_email(email) # this is broken, not pulling the user 

#     return render_template("user_profile.html", user=user)

@app.route("/user_profile")
def display_profile():
    """Displays the user profile"""

    return render_template("user_profile.html")

### ---------------- ROUTES FOR CITY/ACTIVITY PAGE --------------- ###
@app.route("/city_activities/<int:city_id>")
def display_city_activities(city_id):
    """Displays the city with options to view
    restaurants and local attractions"""

    # gets the city object by id. when you get the object you can call city.city in jinja template
    city = crud.get_city_by_id(city_id)

    return render_template("city_activities.html", city=city)


@app.route("/api/restaurants")
def get_restaurants():
    """displays local restaurants"""

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"

    payload = {
        'location' : "-33.8670522,151.1957362",
        'radius':1500,
        'type':"restaurant",
        "key": API_KEY
        }
    headers = {}

    response = requests.get(url, params=payload)

    print(response.text)
    return jsonify(response.text)



@app.route("/api/attractions")
def get_attractions():
    """displays local attractions"""

    # city = crud.get_city_by_name()
    # location = f"{city.latitude},{city.longitude}"

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"

    payload = {
        'location': "-33.8670522,151.1957362",
        'radius': 1500,
        'type': "attraction",
        'key': API_KEY
        }
    headers = {}

    response = requests.get(url, params=payload)
    

    print(response.text)
    return jsonify(response.text)
    

### ---------------- ROUTES FOR ITINERARY PAGE --------------- ###
@app.route("/itineraries")
def display_itineraries():
    """Displays all itineraries created by the user"""
    # itins = get_itins_by_user()

    return render_template("itineraries.html")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
