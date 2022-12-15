from flask import (Flask, render_template, request, session, abort, flash, redirect, url_for)
from dotenv import load_dotenv
import os

load_dotenv()

secret_key = os.getenv("SECRET_KEY")

app = Flask(__name__)

app.secret_key = secret_key

users = {}

@app.route("/")
def home():
    return render_template("home.html", email=session.get("email"))


@app.get("/protected")
def protected():
    if not session.get("email"):
        abort(401)
    return render_template("protected.html")


@app.route("/login", methods=["GET","POST"])
def login():
    email = ""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if users.get("email") == password:
            flash("You are now logged in.")
            session["email"] = email
            return redirect(url_for('home'))
        flash("Incorrect email or password.")

    return render_template("login.html", email=email)



@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        users[email] = password 
        flash("Successfully signed up.")
        return redirect(url_for("login"))
    return render_template("signup.html")



if __name__ == "__main__":
    app.run()
