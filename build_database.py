import os
from datetime import datetime
from config import db
from models import Movies, Director
from directorData import DIRECTOR
from moviesData import MOVIES

if os.path.exists("final_proj.db"):
    os.remove("final_proj.db")

db.create_all()

for director in DIRECTOR:
    d = Director(
        name=director.get("name"),
        id=director.get("id"),
        gender=director.get("gender"),
        uid=director.get("uid"),
        department=director.get("department"),
    )
    db.session.add(d)

for movies in MOVIES:
    m = Movies(
        id=movies.get("id"),
        original_title=movies.get("original_title"),
        budget=movies.get("budget"),
        popularity=movies.get("popularity"),
        release_date=movies.get("release_date"),
        revenue=movies.get("revenue"),
        title=movies.get("revenue"),
        vote_average=movies.get("vote_average"),
        vote_count=movies.get("vote_count"),
        overview=movies.get("overview"),
        tagline=movies.get("tagline"),
        uid=movies.get("uid"),
        director_id=movies.get("director_id"),
    )
    db.session.add(m)

db.session.commit()
