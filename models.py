from datetime import datetime
from config import db, ma
from marshmallow import fields


class Director(db.Model):
    __tablename__ = "directors"
    name = db.Column(db.Text)
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Integer)
    uid = db.Column(db.Integer)
    department = db.Column(db.Text)

    movies = db.relationship(
        "Movies",
        backref="directors",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="asc(Movies.id)",
    )


class Movies(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    original_title = db.Column(db.Text)
    budget = db.Column(db.Integer)
    popularity = db.Column(db.Integer)
    release_date = db.Column(db.Text)
    revenue = db.Column(db.Integer)
    title = db.Column(db.Text)
    vote_average = db.Column(db.Float)
    vote_count = db.Column(db.Integer)
    overview = db.Column(db.Text)
    tagline = db.Column(db.Text)
    uid = db.Column(db.Integer)
    director_id = db.Column(db.Integer, db.ForeignKey("directors.id"))


class DirectorSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Director
        sqla_session = db.session
        load_instance = True

    movies = fields.Nested("DirectorMovieSchema", default=[], many=True)


class DirectorMovieSchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = fields.Int()
    # director_id = fields.Int()
    overview = fields.Str()
    title = fields.Str()


class MovieSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Movies
        sqla_session = db.session
        load_instance = True

    directors = fields.Nested("MovieDirectorSchema", default=None)


class MovieDirectorSchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    director_id = fields.Int()
    name = fields.Str()
    department = fields.Str()
    gender = fields.Int()
