import os
from datetime import datetime
from config import db
from models import Movies, Director

if os.path.exists("final.db"):
    os.remove("final.db")

db.create_all()

db.session.commit()
