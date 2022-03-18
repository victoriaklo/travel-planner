"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb trips")
os.system("createdb trips")

model.connect_to_db(server.app)
model.db.create_all()

# Load city data from JSON file
with open("data/cities_data.json") as f:
    cities_data = json.loads(f.read())

# Create cities, store them in list to create fake itineraries
cities_in_db = []
for city in cities_data:
    city, country, latitude, longitude = (
        city["city"],
        city["country"],
        city["latitude"],
        city["longitude"],
    )

    db_city = crud.create_city(city, country, latitude, longitude)
    cities_in_db.append(db_city)

model.db.session.add_all(cities_in_db)
model.db.session.commit()

# Create 5 users; each user will make 5 ratings
for n in range(5):
    first_name = f"fname{n}"
    last_name = f"lname{n}"
    email = f"user{n}@test.com"  
    password = "test"

    user = crud.create_user(first_name, last_name, email, password)
    model.db.session.add(user)

    # create 5 itineraries per user
    for _ in range(5):
        random_city = choice(cities_in_db)
        title = f"test_title{n}"

        itinerary = crud.create_itinerary(user, title)
        model.db.session.add(itinerary)

model.db.session.commit()

# Create 5 Activities;
for n in range(5):
    name = f"activity{n}"
    type = f"type{n}"
    city_id = randint(1, 10)

    activity = crud.create_activity(name, type, city_id)
    model.db.session.add(activity)

model.db.session.commit()