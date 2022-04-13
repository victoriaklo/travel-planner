import unittest

from server import app
from model import db, example_data, connect_to_db



class TravelandPlanetTest(unittest.TestCase):
    """Tests for my site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_login_page(self):
        result = self.client.get("/")
        self.assertIn(b"Ready to travel the World? Let's plan it!", result.data)
        self.assertNotIn(b"This shouldn't be here!", result.data)

    # def test_user_profile(self):
    #     result = self.client.get("/user_profile")
    #     self.assertIn(b"Email", result.data)
    #     self.assertNotIn(b"This shouldn't be here!", result.data)



class TravelandPlanetTestDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database 
        connect_to_db(app, "postgresql:///testdb", echo=False)

        # Create tables and add sample data
        db.drop_all()
        db.create_all()
        example_data()
    
    def test_login(self):
        result = self.client.post("/login",
                                    data={"email": "test@test.com",
                                        "password": "hello"},
                                    follow_redirects=True)
        self.assertIn(b"Get Started", result.data)
        self.assertNotIn(b"This isn't supposed to be there", result.data)

    def test_itinerary(self):
        login = self.client.post("/login",
                                    data={"email": "test@test.com",
                                        "password": "hello"},
                                    follow_redirects=True)
        result = self.client.get("/itinerary/1", follow_redirects=True)
        self.assertIn(b"title test", result.data)
        self.assertIn(b"Paris attraction: Effiel Tower", result.data)
        self.assertNotIn(b"Where do you want to visit?", result.data)

    
    def test_itinerary_no_login(self):
        result = self.client.get("/itinerary/1", follow_redirects=True)
        self.assertIn(b"Ready to travel the World? Let's plan it!", result.data)
        self.assertIn(b"Email", result.data)
        self.assertNotIn(b"Where do you want to visit?", result.data)

    # ensure that users are only seeing their own created itineraries and not another users
    def test_only_users_itineraries(self):
        login = self.client.post("/login",
                                    data={"email": "test@test.com",
                                        "password": "hello"},
                                    follow_redirects=True)
        result = self.client.get("/itineraries", follow_redirects=True)
        self.assertIn(b"notes test", result.data)
        self.assertIn(b"title test", result.data)
        self.assertNotIn(b"title 11111", result.data)




    def tearDown(self):
        """Do at end of every test."""
        print("test tear down")

        db.session.close()
        db.drop_all()






if __name__ == "__main__":
    unittest.main()
