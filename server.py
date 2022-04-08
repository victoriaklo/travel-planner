"""Server for travel and planning app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, db
import crud
import requests
import os
from datetime import datetime
from passlib.hash import argon2
from itertools import groupby
import re
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "key"
app.jinja_env.undefined = StrictUndefined


# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


API_KEY = os.environ['GOOGLEMAPS_KEY']

### ---------------- ROUTES FOR LOGIN/REGISTER --------------- ###

@app.route("/")
def homepage():
    """View homepage."""

    user_id = session.get('user_email')
    if user_id:
        return redirect('/globe')

    return render_template("login.html")


@app.route("/register", methods=["POST"])
def register_user():
    """Create a new user."""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    hash_password = crud.hash_password(password)
    del password

    pattern = r"\b[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Za-z0-9]{2,}\b"

    if not (re.fullmatch(pattern, email)):
        flash("Please enter a valid email address")
    else:
        user = crud.get_user_by_email(email)
        if user:
            flash("Cannot create an account with that email. Try again.")
        else:
            user = crud.create_user(first_name=first_name, last_name=last_name, email=email, password=hash_password)
            db.session.add(user)
            db.session.commit()
            flash("Account created! Please log in.")

    return redirect("/")


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    pattern = r"\b[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Za-z0-9]{2,}\b"
    if not (re.fullmatch(pattern, email)):
        flash("Please enter a valid email address")
        return redirect("/")

    user = crud.get_user_by_email(email)
    if user:
        #if passwords match, send user to profile
        if argon2.verify(password, user.password):
            session["user_email"] = user.email
            return redirect ("/globe")
        else:
            flash("Sorry, passwords do not match!")
            return redirect('/')
    else:
        flash("Please enter a valid email and password")


@app.route("/logout", methods=["GET", "POST"])
def logout_user():
    """Logout user from session."""

    session.pop('user_email', None)

    return redirect('/')



### ---------------- ROUTES FOR MAIN/GLOBE PAGE --------------- ###

@app.route("/globe")
def render_globe():
    """View Interactive Globe."""

    if not session.get('user_email'):
        return redirect("/")

    return render_template("globe_csv.html")


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

    response = requests.get(url, params=payload).json()
    print(jsonify(response))

    important_data = []

    for item in response["results"]:
        if item["business_status"] == "OPERATIONAL":
            new_dict = {}
            new_dict['name'] = item.get("name")
            new_dict['rating'] = item.get("rating")
            new_dict['place_id'] = item.get("place_id")
            if 'photos' in item:
                photo_ref = item['photos'][0]['photo_reference']
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_ref}&key={API_KEY}"
                new_dict['photo_url'] = photo_url
            important_data.append(new_dict)
    
    return jsonify(results = important_data)



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
        'radius': 50000, # distance in meters ["point_of_interest", "tourist_attraction", "establishment"] 
        'types':["point_of_interest", "tourist_attraction", "landmark", "museum" "natural_feature", "night_club", "establishment"],
        'key': API_KEY
        }
    headers = {}
 # ["amusement_park", "aquarium", "art_gallery","bar", "book_store", "museum", "tourist_attraction", "library", "shopping_mall", "park", "point_of_interest"]
    response = requests.get(url, params=payload).json()

    important_data = []

    for item in response["results"]:
        if item["business_status"] == "OPERATIONAL":
            new_dict = {}
            new_dict['name'] = item.get("name")
            new_dict['rating'] = item.get("rating")
            new_dict['place_id'] = item.get("place_id")
            if 'photos' in item:
                photo_ref = item['photos'][0]['photo_reference']
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_ref}&key={API_KEY}"
                new_dict['photo_url'] = photo_url
            important_data.append(new_dict)
    
    return jsonify(results = important_data)
    

### ---------------- ROUTES FOR ITINERARIES --------------- ###
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


@app.route("/itinerary/<int:id>/edit", methods=["GET","POST"])
def edit_itin_by_id(id):
    """Edit itinerary by id"""

    itinerary = crud.get_itin_by_id(id)
    
    if request.method == 'GET':
        #get the all cities and scheduled activities from itinerary BY itin_id then display it in a form
        # get activity by itin_id, then pass activity to template

        # https://docs.python.org/3/library/itertools.html#itertools.groupby
        sched_acts_grouped_by_city = {}

        for city, sched_acts in groupby(sorted(itinerary.sched_acts, key=lambda sched_act: sched_act.act.city_id), lambda sched_act: sched_act.act.city.city): 
            sched_acts_grouped_by_city[city] = list(sched_acts)

        return render_template("edit-itinerary.html", 
                                itinerary=itinerary, 
                                sched_acts_grouped_by_city=sched_acts_grouped_by_city
                                )

    else:
        # if it's a post request, it is taking the data from the form
        # save the edits and add it to the session, then commit
        form_data = dict(request.form)


        # if notes were added from the form, add to the session
        notes = form_data.get('notes')
        if notes:
            itinerary.notes = notes
            db.session.commit()
            form_data.pop('notes') 


        sched_acts_obj_list = itinerary.sched_acts

        for sched_act_obj in sched_acts_obj_list:

            if str(sched_act_obj.id) in form_data:
                value = form_data[str(sched_act_obj.id)]
                if value:
                    sched_act_obj.datetime = datetime.strptime(value, '%Y-%m-%dT%H:%M')
                    db.session.commit()

        return redirect(f"/itinerary/{id}")

@app.route("/itinerary/<int:itin_id>/delete", methods=["POST"])
def delete_scheduled_activities(itin_id):
    """Deletes scheduled activities by itinerary id"""

    itinerary = crud.get_itin_by_id(itin_id)
    print(itinerary)
    
    sched_acts_list = request.form.getlist("sched-acts-data") #list of act_ids
    print("\n" * 5)
    print(sched_acts_list)
    print("\n" * 5)

    # get itinerary
    # get all sched acts from form
    # then delete sched_activities then commit
    # notes = form_data['notes']
    # form_data.pop('notes')

    list_of_ids = list(map(lambda n: int(n), sched_acts_list))
        
    crud.delete_sched_acts_by_id(list_of_ids)
    flash("----- items permanently deleted -----")

    return redirect(f"/itinerary/{itin_id}")


@app.route("/itinerary/<int:id>")
def display_itin_by_id(id):
    """Display itinerary by id"""
    
    itinerary = crud.get_itin_by_id(id)

    # https://docs.python.org/3/library/itertools.html#itertools.groupby
    sched_acts_by_date = {}

    for key, sched_acts_grouped_by_date in groupby(sorted(itinerary.sched_acts, key=lambda sched_act: str(sched_act.datetime.date()) if sched_act.datetime else ""), lambda sched_act: sched_act.datetime.date() if sched_act.datetime else ""):
        sched_acts_by_date[key] = list(sched_acts_grouped_by_date)


    flights = crud.get_flights_by_itin_id(id) 

    return render_template("itinerary.html", 
                            itinerary=itinerary, 
                            sched_acts_by_date=sched_acts_by_date,
                            flights=flights
                            )


@app.route("/itinerary/<int:id>", methods=["POST"])
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

    all_itineraries = crud.get_itins_by_user(user_id)

    sched_activities_list = []
    for itinerary in all_itineraries:
        sched_activities_list.append(itinerary.sched_acts)
    

    return render_template("itineraries.html", 
                            all_itineraries=all_itineraries,
                            sched_activities_list=sched_activities_list)


@app.route("/itinerary/<int:id>/email")
def email_itinerary(id):
    """Email the itinerary to the user"""

    itinerary = crud.get_itin_by_id(id)

    email = session["user_email"]
    
    itin_data = display_itin_by_id(id)

    start_index = itin_data.index('<div id="itin-body">')
    end_index = itin_data.index("<!-- end of itin div -->")
    itin_body = itin_data[start_index: end_index]



    # call crud function to send email
    email_itinerary_by_id(email, itin_body)
    flash("email has been sent")

    return redirect(f"/itinerary/{id}")

def email_itinerary_by_id(email, data):
    """Takes in itinerary id, and sends email of itinerary"""

    message = Mail(
    from_email='travelandplanet.co@gmail.com',
    to_emails=email,
    subject='Upcoming Trip: Here\'s Your Itinerary',
    html_content=f'{data}')

    print(os.environ.get('SENDGRID_API_KEY'))
    sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)

### ----------- ROUTES FOR FLIGHT ------- ###
@app.route("/itinerary/<int:itin_id>/flights", methods=["GET", "POST"])
def find_flights(itin_id):
    """Find flights for itinerary"""

    if request.method == "GET":
        return render_template("flights.html", itin_id=itin_id)
    else:
        depart_airport = request.form.get("depart-airport")
        depart_datetime = request.form.get("depart-datetime")
        arrival_airport = request.form.get("arrival-airport")
        arrival_datetime = request.form.get("arrival-datetime")

        depart_datetime = datetime.strptime(depart_datetime, '%Y-%m-%dT%H:%M')
        arrival_datetime = datetime.strptime(arrival_datetime, '%Y-%m-%dT%H:%M')

        flight = crud.create_flight(depart_airport, depart_datetime, arrival_airport, arrival_datetime, itin_id)
        db.session.add(flight)
        db.session.commit()

        return redirect(f"/itinerary/{itin_id}")
    

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
