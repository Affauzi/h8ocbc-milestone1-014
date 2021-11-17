import os
from datetime import datetime
from config import db
from models import Movies, Director

if os.path.exists("final_proj.db"):
    os.remove("final_proj.db")

db.create_all()

db.session.commit()
