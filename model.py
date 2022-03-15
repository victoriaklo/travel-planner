"""Models for travel and planning app."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key = True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    #relationships:

    #free attribute '.itins' = a list of Itinerary objects
   

    def __repr__(self):
        return f"<User user_id={self.user_id} first_name ={self.first_name} email={self.email}>"


class Destination(db.Model):
    """A destination"""

    __tablename__ = "destinations"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    city = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    itin_id = db.Column(db.Integer, db.ForeignKey("itineraries.id"), nullable=False)

    #relationships:

    #free attribute '.itin' = a single Itinerary object
    #free attribute '.restaurants' = a list of Restaurant objects
    #free attribute '.attractions' = a list of Attraction objects
    #free attribute '.depart_flight' = a single depart_flight object
    #free attribute '.arrival_flight' = a single arrival_flight object

    def __repr__(self):
        return f"<Destination id={self.id} city={self.city} country={self.country}>"



class Itinerary(db.Model):
    """An itinerary"""

    __tablename__ = "itineraries"

    id = db.Column(db.Integer, autoincrement=True, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    title = db.Column(db.String, nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)

    #relationships:

    user = db.relationship("User", backref="itins")
    dests = db.relationship("Destination", backref="itin") #many-to-one itinerary
    attrs = db.relationship("Attraction", backref="itin") #many-to-one itinerary
    rests = db.relationship("Restaurant", backref="itin") #many-to-one itinerary
    flights = db.relationship("Flight", backref="itin") #many-to-one itinerary

    def __repr__(self):
        return f"<Itinerary id={self.id} user_id={self.user_id} title={self.title}>"



class Restaurant(db.Model):
    """A restaurant"""

    __tablename__ = "restaurants"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    rest_name = db.Column(db.String, nullable=False)
    rest_date = db.Column(db.DateTime)
    dest_id = db.Column(db.Integer, db.ForeignKey("destinations.id"))
    itin_id = db.Column(db.Integer, db.ForeignKey("itineraries.id"))

    #relationships:
    dest = db.relationship("Destination", backref="restaurants")

    #free attribute '.itin' = a single Itinerary object

    def __repr__(self):
        return f"<Restaurant id={self.id} rest_name={self.rest_name}>"



class Attraction(db.Model):
    """An attraction"""

    __tablename__ = "attractions"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    attr_name = db.Column(db.String, nullable=False)
    attr_date = db.Column(db.DateTime)
    dest_id = db.Column(db.Integer, db.ForeignKey("destinations.id"))
    itin_id = db.Column(db.Integer,db.ForeignKey("itineraries.id"))

    # relationships:
    dest = db.relationship("Destination", backref="attractions")

    #free attribute '.itin' = a single Itinerary object

    def __repr__(self):
        return f"<Attraction id={self.id} attr_name={self.attr_name} itin_id={self.itin_id}>"



class Flight(db.Model):
    """A flight"""

    __tablename__ = "flights"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    depart_airport = db.Column(db.String)
    arrival_airport = db.Column(db.String)
    depart_time = db.Column(db.DateTime)
    arrival_time = db.Column(db.DateTime)
    itin_id = db.Column(db.Integer, db.ForeignKey("itineraries.id"))
    depart_dest_id = db.Column(db.Integer, db.ForeignKey("destinations.id")) #one-to-one 
    arrival_dest_id = db.Column(db.Integer, db.ForeignKey("destinations.id")) #one-to-one 
    
    #relationships:
    #free attibute '.itin' = = a list of Itinerary objects
    depart_dest = db.relationship(
                "Destination",
                uselist=False, # means one-to-one
                backref="depart_flight",
                foreign_keys="Flight.depart_dest_id")
    
    arrival_dest = db.relationship(
                "Destination",
                uselist=False,
                backref="arrival_flight",
                foreign_keys="Flight.arrival_dest_id")



    def __repr__(self):
        return f"<Flight id={self.id} itin_id={self.itin_id} depart_dest={self.depart_dest} arrival_dest={self.arrival_dest}>"


def connect_to_db(flask_app, db_uri="postgresql:///trips", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)
    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)