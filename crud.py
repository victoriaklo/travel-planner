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

# get city by name, to get the lat long for api requests
def get_city_by_name(city):
    """Return a city by name"""
    return City.query.filter(City.city==city).first()

### ---------------- CRUD FUNCTIONS FOR ITINERARY --------------- ###

def create_itinerary(user, title ):
    """Create and return a new itinerary."""

    itinerary = Itinerary(
        user=user,
        title=title
        )
    
    return itinerary



def get_itins_by_user(user_id):
    """Get itineraries given a user_id."""

    return Itinerary.query.filter_by(user_id=user_id).all()


# update_itin() <-- can update city, dest, activities, and flights


 
### ---------------- CRUD FUNCTIONS FOR ACTIVITY --------------- ###
def create_activity(name, type, city_id):
    """Create an activity"""

    activity = Activity(
        name=name,
        type=type,
        city_id=city_id
    )

    return activity

 

### ---------------- CRUD FUNCTIONS FOR FLIGHTS --------------- ###
#create_flight



if __name__ == "__main__":
    from server import app

    connect_to_db(app)