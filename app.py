from flask import Flask, redirect, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, bindparam
from datetime import datetime
import random
import os

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///xenocanto.db"
app.config['SECRET_KEY'] = "flash"

db = SQLAlchemy(app)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    birds = [bird["common_name"] for bird in db.session.execute("SELECT * FROM birds")]
    return render_template("/index.html", birds=birds)

@app.route("/show-map", methods=["GET", "POST"])
def show_map():
    if request.method == "POST":
        if request.form.get("action") == "search":

            if not request.form.get("species"):
                return redirect("/")

            species = request.form.get("species").lower()
            query = text("SELECT * FROM birds WHERE sci_name=:species OR common_name=:species OR short_name=:species").bindparams(species=species)
            results = [row for row in db.session.execute(query)]

            if len(results) == 0:
                flash("Species \"" + species + "\" not found", "danger")
                return redirect("/")

            else:
                bird_id = results[0]["id"]

                query = text("SELECT lat, long, recording_date FROM recordings WHERE bird_id=:bird_id").bindparams(bird_id=bird_id)
                recordings = [row for row in db.session.execute(query)]

                query = text("SELECT sci_name, common_name FROM birds WHERE id=:bird_id").bindparams(bird_id=bird_id)
                names = [row for row in db.session.execute(query)]

                sci_name = names[0]["sci_name"]
                common_name = names[0]["common_name"]

                lat = []
                lon = []
                date_ind = []
                date_str = []

                for recording in recordings:
                    lat.append(recording["lat"])
                    lon.append(recording["long"])

                    try:
                        recording_datetime = datetime.strptime(recording["recording_date"].split()[0][5:], "%m-%d")
                    except:
                        recording_datetime = datetime.strptime("02-28", "%m-%d")
                    starting_datetime = datetime.strptime("01-01", "%m-%d")
                    date_ind.append((recording_datetime-starting_datetime).days)
                    date_str.append(recording_datetime.strftime('%b %-m'))

                title = "Geographic range distribution for <br>" + common_name + " (<i>" + sci_name.capitalize() + "<i>)"

                return render_template('/plotlyshow.html', lat=lat, lon=lon, date_ind=date_ind, date_str=date_str, title=title)

        else:
            num_birds = [row for row in db.session.execute("SELECT COUNT(id) FROM birds")][0]["COUNT(id)"]
            bird_id = random.randint(1, num_birds)

            query = text("SELECT lat, long, recording_date FROM recordings WHERE bird_id=:bird_id").bindparams(bird_id=bird_id)
            recordings = [row for row in db.session.execute(query)]

            query = text("SELECT sci_name, common_name FROM birds WHERE id=:bird_id").bindparams(bird_id=bird_id)
            names = [row for row in db.session.execute(query)]

            sci_name = names[0]["sci_name"]
            common_name = names[0]["common_name"]

            lat = []
            lon = []
            date_ind = []
            date_str = []

            for recording in recordings:
                lat.append(recording["lat"])
                lon.append(recording["long"])

                try:
                    recording_datetime = datetime.strptime(recording["recording_date"].split()[0][5:], "%m-%d")
                except:
                    recording_datetime = datetime.strptime("02-28", "%m-%d")
                starting_datetime = datetime.strptime("01-01", "%m-%d")
                date_ind.append((recording_datetime - starting_datetime).days)
                date_str.append(recording_datetime.strftime('%b %-m'))

            title = "Geographic range distribution for <br>" + common_name + " (<i>" + sci_name.capitalize() + "<i>)"

            return render_template('/plotlyshow.html', lat=lat, lon=lon, date_ind=date_ind, date_str=date_str,
                                   title=title)
    else:
        return redirect("/")

if __name__=="__main__":
    app.run(debug=True)