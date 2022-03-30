"""CRUD operations."""

from model import db, User, City, Itinerary, Destination, Activity, ScheduledActivity, connect_to_db

### ---------------- CRUD FUNCTIONS FOR USER --------------- ###

def create_user(first_name, last_name, email, password):
    """Create and return a new user."""

    user = User(first_name=first_name, last_name=last_name, email=email, password=password)

    return user


def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return user by email
     --needed to check if user in session from the server.py
    """

    return User.query.filter(User.email == email).first()


### ---------------- CRUD FUNCTIONS FOR CITY --------------- ###

# def get_city(from the static list in the database)
def create_city(city, country, latitude, longitude):
    """Create a city for the database"""

    city = City(
        city=city,
        country=country,
        latitude=latitude,
        longitude=longitude
    )

    return city

def get_cities():
    """Return all cities."""

    return City.query.all()


def get_city_by_id(city_id):
    """Return a city by primary key."""

    return City.query.get(city_id)


def get_city_by_name(city):
    """Return a city by name"""
    return City.query.filter(City.city == city).first()

### ---------------- CRUD FUNCTIONS FOR DESTINATION --------------- ###
def create_destination(city_id, itin_id):
    """Create and return a new itinerary."""

    destination = Destination(
        city_id=city_id,
        itin_id=itin_id
        )
    
    return destination

### ---------------- CRUD FUNCTIONS FOR ITINERARY --------------- ###

def create_itinerary(user_id, title):
    """Create and return a new itinerary."""

    itinerary = Itinerary(
        user_id=user_id,
        title=title
        )
    
    return itinerary

def get_itin_by_id(id):
    """Get itinerary by id."""

    return Itinerary.query.get(id)

def get_itins_by_user(user_id):
    """Get itineraries given a user_id."""

    return Itinerary.query.filter_by(user_id=user_id).all()

def delete_itin_by_id(id):
    """Delete an itinerary by id"""
    itin_object = Itinerary.query.get(id)
    sched_act_list = itin_object.sched_acts
    for item in sched_act_list:
        db.session.delete(item)
    db.session.delete(itin_object)
    db.session.commit()


 
### ---------------- CRUD FUNCTIONS FOR ACTIVITY --------------- ###
def create_activity(name, type, city_id):
    """Create an activity"""

    activity = Activity(
        name=name,
        type=type,
        city_id=city_id
    )

    return activity

def get_activity_by_id(id):
    """Get activity by id."""

    return Activity.query.get(id).first()

def get_activity_by_name(name):
    """Get activity by id."""

    return Activity.query.filter(Activity.name==name).first()

# crud function filter all activities by city then by name
# filter by cityID. build up a chain of filters to get the activity
# return all

def get_activities_by_activities_ids(ids):
    """Get a list of activities by ids"""

    return Activity.query.filter(Activity.id.in_(ids)).all()

### ---------------- CRUD FUNCTIONS FOR SCHEDULED ACTIVITY --------------- ###
 
def create_sched_activity(act_id,itin_id):
    """Create an activity"""

    sched_act = ScheduledActivity(
        act_id=act_id,
        itin_id=itin_id
    )

    return sched_act


### ---------------- CRUD FUNCTIONS FOR FLIGHTS --------------- ###
#create_flight



if __name__ == "__main__":
    from server import app

    connect_to_db(app)