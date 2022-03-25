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
        return redirect('/main')

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

    if not session.get('user_email'):
        return redirect("/")

    return render_template("main.html")


@app.route("/logout", methods=["GET", "POST"])
def logout_user():
    """Logout user from session."""

    session.pop('user_email', None)

    return redirect('/')



### ---------------- ROUTES FOR MAIN/GLOBE PAGE --------------- ###


### ---------------- ROUTES FOR USER PROFILE PAGE --------------- ###

@app.route("/user_profile")
def display_profile():
    """Displays the user profile"""

    if not session.get('user_email'):
        return redirect("/")
    
    email = session.get('user_email')
    
    user = crud.get_user_by_email(email)
    

    return render_template("user_profile.html", user=user)

### ---------------- ROUTES FOR CITY/ACTIVITY PAGE --------------- ###

@app.route("/city_activities/<int:city_id>")
def display_city_activities_by_id(city_id):
    """Displays the city with options to view
    restaurants and local attractions"""

    if not session.get('user_email'):
        return redirect("/")

    # gets the city object by id
    city = crud.get_city_by_id(city_id)
    # get list of itineraries by their titles and id and pass it to template
    email = session.get('user_email')
    user = crud.get_user_by_email(email)
    user_id = user.user_id

    itinerary_list = crud.get_itins_by_user(user_id)

    return render_template("city_activities.html", city=city, itinerary_list=itinerary_list)


@app.route("/api/restaurants")
def get_restaurants():
    """displays local restaurants"""

    if not session.get('user_email'):
        return redirect("/")
    
    city_id = request.args.get('city_id')

    city = crud.get_city_by_id(city_id)

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"

    payload = {
        'location' : f"{city.latitude},{city.longitude}",
        'radius':50000,
        'type':"restaurant",
        "key": API_KEY
        }
    headers = {}

    response = requests.get(url, params=payload)

    print(response.text)
    return jsonify(response.text)



@app.route("/api/attractions/")
def get_attractions():
    """displays local attractions"""

    city_id = request.args.get('city_id')
    print(city_id)

    if not session.get('user_email'):
        return redirect("/")
    

    city = crud.get_city_by_id(city_id)
    print(city)
    # get the placeID
    # store it in the activityTable

    location = f"{city.latitude},{city.longitude}"

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"

    payload = {
        'location': location,
        'radius': 50000, # distance in meters
        'types':[ "museum", "tourist_attraction", "art_gallery", "bar", "shopping_mall", "park" ],
        'key': API_KEY
        }
    headers = {}

    response = requests.get(url, params=payload)
    

    print(response.text)
    return jsonify(response.text)
    

### ---------------- ROUTES FOR ITINERARY PAGE --------------- ###
@app.route("/new_itinerary", methods=["POST"])
def create_itinerary():
    """Display itinerary made by user"""

    # if the user is in session, display only the user's itineraries
    if session.get('user_email'):
        email = session['user_email']
        user = crud.get_user_by_email(email)
    else:
        return redirect("/")

    city_id = request.form.get("city_id")
    
    city = crud.get_city_by_id(city_id) # city is the City object
    rest_list = request.form.getlist("rest-choice")
    attr_list = request.form.getlist("attr-choice")

    user_id = user.user_id
    title = request.form.get("title")
    new_itinerary = crud.create_itinerary(user_id, title)

    db.session.add(new_itinerary)
    db.session.commit()

    itin_id = new_itinerary.id

    dest = crud.create_destination(city_id, itin_id)
    db.session.add(dest)
    db.session.commit()

    activities_dict = {
    "restaurant": rest_list,
    "attraction": attr_list
    }


    for key, value in activities_dict.items():
        for item in value:
            check_activity = crud.get_activity_by_name(item)

            if check_activity is None:
                new_activity = crud.create_activity(item, key, city_id)
                db.session.add(new_activity)
                db.session.commit()
                act_id = new_activity.id
           
            else:
                act_id = check_activity.id

            sched_act = crud.create_sched_activity(act_id, itin_id)
            db.session.add(sched_act)
            db.session.commit()


    # get activity, check if activity exists, do not add, else add

    return render_template("new_itinerary.html", 
                            city=city,
                            rest_list=rest_list,
                            attr_list=attr_list,
                            new_itinerary=new_itinerary,
                            title=title
                            )




@app.route("/update_itinerary", methods=["POST"])
def update_itinerary():
    """Update existing itinerary with other activities or flights"""

    itin_id = request.form.get("update-itinerary")
    rest_list = request.form.getlist("rest-choice")
    attr_list = request.form.getlist("attr-choice")
    city_id = request.form.get("city_id")

    # what if multiple names in multiple cities?
    # create a crud function to get activity
        # crud.get_by_city_id(city_id).get_activity_by_name(item)
        # result of this will be the activities to check against

    activities_dict = {
        "restaurant": rest_list,
        "attraction": attr_list
        }


    for key, value in activities_dict.items():
        for item in value:
            check_activity = crud.get_activity_by_name(item)

            if check_activity is None:
                new_activity = crud.create_activity(item, key, city_id)
                db.session.add(new_activity)
                db.session.commit()
                act_id = new_activity.id
            
            else:
                act_id = check_activity.id
                
            sched_act = crud.create_sched_activity(act_id, itin_id)
            db.session.add(sched_act)
            db.session.commit()
    
   
    return redirect(f"/itinerary/{itin_id}")



@app.route("/itinerary/<int:id>")
def display_itin_by_id(id):
    """Display itinerary by id"""
    
    itinerary = crud.get_itin_by_id(id)
    # get activity by itin_id, then pass activity to template
    activities_ids = []

    for sched_act in itinerary.sched_acts:
        activities_ids.append(sched_act.act_id)

    activities = crud.get_activities_by_activities_ids(activities_ids)

    act_group_by_city = {}
    for activity in activities:
        if activity.city_id in act_group_by_city:
            # append activity at that key
            act_group_by_city[activity.city_id].append(activity)
        else:
            act_group_by_city[activity.city_id] = [activity]


    return render_template("itinerary.html", 
                            itinerary=itinerary, 
                            activities=activities, 
                            act_group_by_city=act_group_by_city
                            )


@app.route("/itinerary/<int:id>", methods = ["DELETE"])
def delete_itin_by_id(id):
    """Delete an itinerary by id"""
    crud.delete_itin_by_id(id)
    flash("Itinerary deleted")

    return redirect("/itineraries")




@app.route("/itineraries")
def display_itineraries():
    """Displays all itineraries created by the user"""

    # if the user is in session, display only the user's itineraries
    if session.get('user_email'):
        email = session['user_email']
        user = crud.get_user_by_email(email)
    else:
        return redirect("/")

    user_id = user.user_id

    # returns a list of itinerary objects
    # query all itins for current user, then pass that list of itineraries to jinja template
    # then using the relationships to get the other info you need

    all_itineraries = crud.get_itins_by_user(user_id)

    sched_activities_list = []
    for itinerary in all_itineraries:
        sched_activities_list.append(itinerary.sched_acts)
    

    return render_template("itineraries.html", 
                            all_itineraries=all_itineraries,
                            sched_activities_list=sched_activities_list)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
