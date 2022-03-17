"""Models for travel and planning app."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# # # https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#many-to-many
# destinations = db.Table('destinations', 
# db.Column('itin_id', db.Integer, db.ForeignKey('itineraries.id'), primary_key =True),
# db.Column('city_id', db.Integer, db.ForeignKey('cities.id'), primary_key =True))

# # how do you get the destinations table to link to city and itinerary tables in the database? 



class User(db.Model):
    """A user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key = True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    #relationships:
    
    #free attribute: 'itins' = a list of itinerary objects
   

    def __repr__(self):
        return f"<User user_id={self.user_id} first_name ={self.first_name} email={self.email}>"

# test_user = User(first_name='V', last_name='lo', email='hi@hi.com', password='hello')
# db.session.add(test_user)


class City(db.Model):
    """A city"""

    __tablename__ = "cities"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    city = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)



    #relationships:

    #free attribute: 'itins' = a list of itinerary objects
    activity = db.relationship("Activity", uselist=False, back_populates="city")


    def __repr__(self):
        return f"<City id={self.id} city={self.city} country={self.country}>"

# test_city = City(city="sf", country="USA", latitude=1.00, longitude=-1.00)
# db.session.add(test_city)
# db.session.commit()


class Itinerary(db.Model):
    """An itinerary"""

    __tablename__ = "itineraries"

    id = db.Column(db.Integer, autoincrement=True, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    title = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date) 
    end_date = db.Column(db.Date)
    notes = db.Column(db.Text)

    #relationships:

    user = db.relationship("User", backref="itins") # one-to-many itineraries
    cities = db.relationship("City", secondary="destinations", backref="itins") #many-to-many
    # flights = db.relationship("Flight", backref="itin") #many-to-one itinerary

    #free attribute: 'sched_acts' = a list of scheduled activity objects


    def __repr__(self):
        return f"<Itinerary id={self.id} user_id={self.user_id} title={self.title}>"

# test_itin = Itinerary(user_id=1, title='tokyo', notes="vacation forever")
# db.session.add(test_itin)
# db.session.commit()


class Destination(db.Model):
    """A destination - association table to city and itinerary"""

    __tablename__ = "destinations"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey("cities.id"), nullable=False)
    itin_id = db.Column(db.Integer, db.ForeignKey("itineraries.id"),nullable=False)




    def __repr__(self):
        return f"<Destination id={self.id} city_id={self.city} itin_id={self.itin_id}>"

# test_dest = Destination(city_id =1, itin_id=1)
# db.session.add(test_dest)

class Activity(db.Model):
    """An activity"""

    __tablename__ = "activities"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey("cities.id"), nullable=False)

    #relationships:

    #free attribute: 'sched_acts' = a list of scheduled activity objects
    city = db.relationship("City", uselist = False, back_populates="activity")
    


    def __repr__(self):
        return f"<Activity id={self.id} name={self.name} type={self.type}>"

# test_act = Activity(name="warped tour", type="festival", city_id="1")
# db.session.add(test_act)
# db.session.commit()


class ScheduledActivity(db.Model):
    """A middle table for itinerary and activity"""

    __tablename__ = "sched_acts"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    act_id = db.Column(db.Integer, db.ForeignKey("activities.id"), nullable=False)
    itin_id = db.Column(db.Integer, db.ForeignKey("itineraries.id"), nullable=False)
    datetime = db.Column(db.DateTime) # format -> datetime(YYYY, MM, DD, HH, MM, SS, MS)
    # https://docs.python.org/3/library/datetime.html#datetime-objects

    #relationships:
    act = db.relationship("Activity", backref="sched_acts")
    itin = db.relationship("Itinerary", backref="sched_acts")


    def __repr__(self):
        return f"<ScheduledActivity id={self.id} act_id={self.act_id} itin_id={self.itin_id}>"

#test_sched = ScheduledActivity(act_id=1, itin_id=1, datetime=datetime(2019, 6, 5, 8, 10, 10, 10))
# db.session.add(test_sched)
# db.session.commit()



# class Flight(db.Model):
#     """A flight"""

#     __tablename__ = "flights"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     depart_airport = db.Column(db.String)
#     arrival_airport = db.Column(db.String)
#     depart_time = db.Column(db.DateTime)
#     arrival_time = db.Column(db.DateTime)
#     itin_id = db.Column(db.Integer, db.ForeignKey("itineraries.id")) 
#     depart_city_id = db.Column(db.Integer, db.ForeignKey("cities.id")) #one-to-one 
#     arrival_city_id = db.Column(db.Integer, db.ForeignKey("cities.id")) #one-to-one 
    
#     #relationships:

#     #free attribute '.itin' = = a list of Itinerary objects

#     depart_city_id = db.relationship(
#                 "Destination",
#                 uselist=False, # means one-to-one
#                 backref="depart_flight",
#                 foreign_keys="Flight.depart_city_id")
    
#     arrival_city_id = db.relationship(
#                 "Destination",
#                 uselist=False,
#                 backref="arrival_flight",
#                 foreign_keys="Flight.arrival_city_id")



#     def __repr__(self):
#         return f"<Flight id={self.id} itin_id={self.itin_id} depart_city_id={self.depart_city_id} arrival_city_id={self.arrival_city_id}>"

#test_flight = Flight(depart_airport="sfo", arrival_airport="cdg", itin_id=1, depart_city_id=1, arrival_city_id=1)


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
