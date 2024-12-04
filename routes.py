from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Vote
from flask_migrate import Migrate
from datetime import datetime
import os
from sqlalchemy import desc

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///votes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your_secret_key_here"

db.init_app(app)
migrate = Migrate(app, db)


def create_tables():
    with app.app_context():
        db.create_all()
        print(f"Database file created at: {app.config['SQLALCHEMY_DATABASE_URI']}")


@app.route("/")
def index():
    return render_template("index.html", the_title="Student Government Voting System")


@app.route("/vote", methods=["GET", "POST"])
def vote():
    if request.method == "POST":
        name = request.form["name"]
        gender = request.form["gender"]
        course = request.form["course"]
        date = datetime.strptime(request.form["date"], "%Y-%m-%d")
        candidate = request.form["candidate"]

        if Vote.query.filter_by(name=name).first():
            flash("You have already voted!", "error")
            return redirect(url_for("vote"))

        new_vote = Vote(
            name=name, gender=gender, course=course, date=date, candidate=candidate
        )
        try:
            db.session.add(new_vote)
            db.session.commit()
            print(f"Vote saved: {new_vote}")
            flash("Your vote has been recorded successfully!", "success")
        except Exception as e:
            print(f"Error saving vote: {str(e)}")
            db.session.rollback()
            flash("There was an error saving your vote. Please try again.", "error")

        return redirect(url_for("thank_you"))

    return render_template("vote.html", the_title="Cast Your Vote")


@app.route("/thank_you")
def thank_you():
    return render_template("thank_you.html", the_title="Thank You for Voting")


@app.route("/results")
def results():
    total_votes, gender_stats, course_stats, candidate_stats = (
        Vote.get_vote_statistics()
    )
    return render_template(
        "results.html",
        the_title="Voting Results",
        total_votes=total_votes,
        gender_stats=gender_stats,
        course_stats=course_stats,
        candidate_stats=candidate_stats,
    )


@app.route("/voters")
def voters():
    voters_list = Vote.query.order_by(desc(Vote.date)).all()
    return render_template("voters.html", the_title="Voters List", voters=voters_list)


if __name__ == "__main__":
    create_tables()
    print(f"Current working directory: {os.getcwd()}")
    print(f"Instance folder path: {app.instance_path}")
    app.run(debug=True)
