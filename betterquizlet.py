from flask import Flask, flash, render_template, request
from apscheduler.scheduler import Scheduler
import sqlite3 as sql
import atexit


app = Flask(__name__)
app.secret_key = "random string"

@app.route("/makesets")
def make_sets():
    return render_template("makesets.html")

@app.route("/studysets")
def study_sets():
    return render_template("studysets.html")
    

@app.route("/")
def home():
    conn = sql.connect("database.db")
    #when the user enters a word, store it in a table with the definition that they also enter
    #then when you test them, if their answer at the moment matches with what they entered, that is how you know you got it correct
    #so store the word and definition in a table but do not display that table to the user, that is just for us to check against 
    conn.execute(
        "CREATE TABLE IF NOT EXISTS words (word TEXT)"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS definitions (definition TEXT)"
    )
    conn.execute (
        "CREATE TABLE IF NOT EXISTS reviews (userreview TEXT)"
    )
    conn.execute (
        "CREATE TABLE IF NOT EXISTS questions (useremail TEXT, usermessage TEXT)"
    )
    conn.close()
    return render_template("home.html")


@app.route("/reviews")
def view_reviews():
    return render_template("reviews.html")

@app.route('/savereviews', methods = ["POST"])
def save_reviews():
    if request.method == "POST":
        user_review = request.form["theuserreview"]
        conn = sql.connect("database.db")
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO reviews (userreview) VALUES (?)",
            (user_review,)
        )
        conn.commit()
        flash(
            "Thank you for submitting your review! Enjoy the app.")
        return render_template("reviews.html")



@app.route("/askquestions", methods=["POST"])
def save_questions():
    if request.method == "POST":
        emailaddr = request.form["email"]
        usermessage = request.form["message"]
        conn = sql.connect("database.db")
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO questions (useremail,usermessage) VALUES (?,?)",
            (emailaddr, usermessage),
        )
        conn.commit()
        flash(
            "Thank you for submitting your question. We will get back to you shortly!"
        )
        return render_template("askquestions.html")


if __name__ == "__main__":
    app.run(debug=True)

