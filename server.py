"""Server for travel and planning app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, db
import crud
import requests

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "key"
app.jinja_env.undefined = StrictUndefined

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
        return redirect("/homepage")


@app.route("/homepage")
def render_mainpage():
    """Renders main page"""
    return render_template("main.html")



### ---------------- ROUTES FOR MAIN/GLOBE PAGE --------------- ###

### ---------------- ROUTES FOR USER PROFILE PAGE --------------- ###
@app.route("/user_profile")
def display_profile():
    """Displays the user profile"""

    return render_template("user_profile.html")

### ---------------- ROUTES FOR ACTIVITY PAGE --------------- ###
# @app.route("/api/tuition")
# def get_tuition():
#   """Return information about tuition as JSON."""

#   return jsonify({"tuition": 1000})



### ---------------- ROUTES FOR ITINERARY PAGE --------------- ###
# @app.route("/itineraries")
# def display_itineraries():
#     """Displays all itineraries created by the user"""
#     itins = get_itins_by_user()

#     return render_template("itineraries.html", itins=itins)


@app.route("/api/restaurants")
def get_restaurants():
    """displays local restaurants"""

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522%2C151.1957362&radius=1500&type=restaurant&keyword=cruise&key=AIzaSyCTDuA7WxlJXqgH98H7FHP5e8jMeSD1ZtQ"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    return jsonify(response.text)



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
