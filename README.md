# Travel and Planet
Ready for your next trip? Plan it with Travel and Planet. 

Travel and Planet is a new and interactive way to plan your next trip. This web app will have three core capabilities: pick a destination, select local activities, and build an itinerary. There are 100 popular destinations around the world to choose from. Once a user selects their destination, they will be able to select local restaurants and attractions and build an itinerary. After adding items to their itinerary, users can add dates and times, delete items, and even add flight information. Finally, users can email their itinerary to themselves and enjoy their next vacation.

# Table of Contents
* 🤖 [Technologies Used](https://github.com/victoriaklo/travel-planner #Technologies Used)
* 🗺 [Features](https://github.com/victoriaklo/travel-planner "Features")
* 💡 [Future Improvements](https://github.com/victoriaklo/travel-planner "Future Improvements")
* 🔌 [Set Up](https://github.com/victoriaklo/travel-planner "Set Up")
* 👩🏻‍💻 [About Me](https://github.com/victoriaklo/travel-planner "About Me")

# Technologies Used
Backend: Python, Flask, PostgreSQL, SQLAlchemy \
Frontend: Javascript, HTML, CSS, Bootstrap, AJAX, JSON, Jinja2 \
APIs: ArcGIS API, Google Places API, Sendgrid API

# Features
* Create an account, then log in.
* Emails are format-validated using regex Python library
* Passwords are hashed in the database for added security
* Using the ArcGIS API, create an interactive globe to find a destination.
* Using a CSV list, there are 100 markers with preset destinations.
* A pop-up modal appears when the marker is clicked.
* Users can click a button in the pop-up modal to select this destination and find local restaurants and attractions.
* Using Google Places API and an AJAX call to populate a list of restaurants and attractions without needing to reload the page. 
* Users can either create a new itinerary or update an existing itinerary
* All items in the itinerary can be edited by adding datetime, flight information, and adding notes. 
* Users can also delete parts of an itinerary or the whole itinerary.
* The itinerary will be grouped by city and sorted by date.
* Using the Sendgrid’s API, users can email their itinerary to their account email.

# Future Improvements
* Adding other AJAX requests to compile all editing and adding items to one page. This will create a more seamless user experience when editing an itinerary.
* Using Google Place API to find photo URLs of each 100 destinations and save them in my database. Then, I can display dynamic images on each itinerary based on the destination a user chooses.

# Set Up
To run this project, first clone or fork this repo:

`git clone https://github.com/victoriaklo/travel-planner.git`
 
Create and activate a virtual environment inside your directory:
```
virtualenv env
source env/bin/activate
```
 
Install the dependencies:

`pip3 install -r requirements.txt`
 
Sign up to obtain keys for the ArcGIS API, Google Places API, and Sendgrid API.

ArcGIS API key will be added to your HTML template, you can restrict your API from specific clients from the ArcGIS dashboard.

Save your Google API keys in a file called secrets.sh using this format:

`export APP_KEY="YOUR_KEY_GOES_HERE"`

Save your Sendgrid API keys in a file called sendgrid.env using this format:

`export SENDGRID_API_KEY="YOUR_KEY_GOES_HERE"`
 
Source your keys into your virtual environment:
```
source secrets.sh
source sendgrid.env
```

 
Set up the database:
`python3 model.py`


Seed the data to the database:
`python3 seed_database.py`
 
Run the app:
`python3 server.py`
 
You can now navigate to `localhost:5000/` to access the app


# About Me
👩🏻‍💻  Hi everyone, I’m Victoria — a software engineer from San Francisco, CA. Following Agile methodologies, I completed this web app in two 2-week sprints as my capstone project for Hackbright Academy's full-stack software engineering program. If you have any questions about my project or would like to connect, feel free to contact me on [LinkedIn](https://www.linkedin.com/in/victoria-lo/).
