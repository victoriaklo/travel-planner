"""CRUD operations."""

from model import db, User, City, Itinerary, Activity, connect_to_db

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
# def create_itinerary() <-- links itin to city, itin to dest, activities

# update_itin()



### ---------------- CRUD FUNCTIONS FOR ACTIVITY --------------- ###
#create_activity
### ---------------- CRUD FUNCTIONS FOR FLIGHTS --------------- ###


if __name__ == "__main__":
    from server import app

    connect_to_db(app)