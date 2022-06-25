import csv
import sqlite3
from datetime import datetime

open("xenocanto.db", "w").close()
con = sqlite3.connect("xenocanto.db")
db = con.cursor()

db.execute("CREATE TABLE birds (id INTEGER, " +
                                "sci_name TEXT NOT NULL UNIQUE, " +
                                "common_name TEXT NOT NULL UNIQUE, " +
                                "short_name TEXT NOT NULL UNIQUE, " +
                                "PRIMARY KEY(id))")

db.execute("CREATE TABLE recordings (id INTEGER, " +
                                    "bird_id INTEGER NOT NULL, " +
                                    "lat NUMERIC NOT NULL, " +
                                    "long NUMERIC NOT NULL, " +
                                    "recording_date DATE NOT NULL, " +
                                    "PRIMARY KEY(id), " +
                                    "FOREIGN KEY(bird_id) REFERENCES birds(id))")

with open("xenocanto.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        db.execute("INSERT OR IGNORE INTO birds (sci_name, common_name, short_name) VALUES (?, ?, ?)",
                         (row["scientific_name"].lower(), row["common_name"].lower(),
                          row["primary_label"].strip(",'0123456789").lower())
                  )
con.commit()

with open("xenocanto.csv", "r") as file:
    reader = csv.DictReader(file)
    count = 0
    for row in reader:
        birds = [x.strip(",'0123456789").lower() for x in row["secondary_labels"].strip("[]").split()]
        birds.append(row["primary_label"].strip(",'0123456789").lower())

        lat = float(row["latitude"])
        long = float(row["longitude"])

        try:
            date = datetime.strptime(row["date"], '%Y-%m-%d')
        except:
            continue

        for bird in birds:
            bird_id = list(db.execute("SELECT id FROM birds WHERE short_name = ?", [bird]))[0][0]
            db.execute("INSERT INTO recordings (bird_id, lat, long, recording_date) VALUES (?, ?, ?, ?)",
                        (bird_id, lat, long, date))
con.commit()