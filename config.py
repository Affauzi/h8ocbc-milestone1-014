import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))


# Create the Connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app

# Configure the SQLAlchemy part of the app instance
app.config["SQLALCHEMY_ECHO"] = True
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
#     basedir, "final_proj.db"
# )
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://elxsgrhpxlfdrt:e11edaf4b0351f83c4bd5e352e25cf96f4fd8ab73cb7a9960e25ff8d0f5774c2@ec2-34-203-114-67.compute-1.amazonaws.com:5432/db4bh64tk54ck6"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)
