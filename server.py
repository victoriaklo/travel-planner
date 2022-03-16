"""Server for travel and planning app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "key"
app.jinja_env.undefined = StrictUndefined

### ---------------- ROUTES FOR HOME/LOGIN --------------- ###

@app.route("/")
def homepage():
    """View homepage."""

    user_id = session.get('user_email')
    if user_id:
        return redirect('/login')

    return render_template("homepage.html")


@app.route("/register", methods=["POST"])
def register_user():
    """Create a new user."""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(first_name, last_name, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")



@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        return redirect("/")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        return redirect("/homepage")


@app.route("/homepage")
def render_mainpage():
    return render_template("main.html")



### ---------------- ROUTES FOR MAIN PAGE --------------- ###


    



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
