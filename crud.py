"""CRUD operations."""

from model import db, User, City, Itinerary, Destination, Activity, connect_to_db

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

### ---------------- CRUD FUNCTIONS FOR DESTINATION --------------- ###



### ---------------- CRUD FUNCTIONS FOR CITY --------------- ###
# def get_city(from the static list in the database)


### ---------------- CRUD FUNCTIONS FOR ITINERARY --------------- ###
# def create_itinerary() <-- links itin to city, dest, activities

def create_itinerary(user, cities, sched_acts):
    """Create and return a new itinerary."""

    itin = Itinerary(user=user, cities=cities, sched_acts=sched_acts)
    

    return itin


def get_itins_by_user(user_id):
    """Get itineraries given a user_id."""

    return Itinerary.query.filter_by(user_id=user_id).all()


# update_itin() <-- can update city, dest, activities, and flights



### ---------------- CRUD FUNCTIONS FOR ACTIVITY --------------- ###
#create_activity


### ---------------- CRUD FUNCTIONS FOR FLIGHTS --------------- ###
#create_flight



if __name__ == "__main__":
    from server import app

    connect_to_db(app)