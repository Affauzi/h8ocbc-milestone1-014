"""
This is the director module and supports all the REST actions for the
director data
"""

from flask import make_response, abort, jsonify
from config import db
from models import Director, DirectorSchema, Movies
from sqlalchemy.orm import load_only, query
from sqlalchemy.sql import func


def read_all(limitation):
    """
    This function responds to a request for /api/director
    with the complete lists of director

    :return:        json string of list of director
    """
    # Create the list of director from our data
    director = Director.query.order_by(Director.id).limit(limitation).all()

    # Serialize the data for the response
    director_schema = DirectorSchema(many=True)
    data = director_schema.dump(director)
    return data


def read_one(id):
    """
    This function responds to a request for /api/director/{id}
    with one matching director from directors

    :param id:   Id of director to find
    :return:            director matching id
    """
    # Build the initial query
    director = Director.query.filter(Director.id == id).outerjoin(Movies).one_or_none()

    if director is not None:

        # Serialize the data for the response
        director_schema = DirectorSchema()
        data = director_schema.dump(director)
        return data

    else:
        abort(404, f"Director not found for Id: {id}")


def create(director):
    """
    This function creates a new director in the directors structure

    :param director:  director to create in directors structure
    :return:        201 on success, 406 on director exists
    """
    id = director.get("id")

    existing_director = Director.query.filter(Director.id == id).one_or_none()

    # Can we insert this director?
    if existing_director is None:

        # Create a director instance using the schema and the passed in director
        schema = DirectorSchema()
        new_director = schema.load(director, session=db.session)

        # Add the director to the database
        db.session.add(new_director)
        db.session.commit()

        # Serialize and return the newly created director in the response
        data = schema.dump(new_director)

        return data, 201

    # Otherwise, nope, director exists already
    else:
        abort(409, f"Director {id} exists already")


def update(id, director):
    """
    This function updates an existing director in the directors structure

    :param id:   Id of the director to update in the directors structure
    :param director:      director to update
    :return:            updated director structure
    """
    # Get the director requested from the db into session
    update_director = Director.query.filter(Director.id == id).one_or_none()

    # Did we find an existing director?
    if update_director is not None:

        # turn the passed in director into a db object
        schema = DirectorSchema()
        update = schema.load(director, session=db.session)

        # Set the id to the director we want to update
        update.id = update_director.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated director in the response
        data = schema.dump(update_director)

        return data, 200

    # Otherwise, nope, didn't find that director
    else:
        abort(404, f"Director not found for Id: {id}")


def delete(id):
    """
    This function deletes a director from the directors structure

    :param id:   Id of the director to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the director requested
    director = Director.query.filter(Director.id == id).one_or_none()

    # Did we find a director?
    if director is not None:
        db.session.delete(director)
        db.session.commit()
        return make_response(f"Director {id} deleted", 200)

    # Otherwise, nope, didn't find that director
    else:
        abort(404, f"Director not found for Id: {id}")


def film_budget():
    """
    This function responds to a request for /api/director
    with the complete lists of director

    :return:        json string of list of director
    """

    # query Director Budget in director class:
    # select d.name, sum(m.budget) from movies m, directors d
    # where m.director_id = d.id
    # GROUP BY d.name
    # ORDER BY sum(m.budget) DESC

    director = (
        db.session.query(Director.name, func.sum(Movies.budget).label("budget"))
        .join(Movies)
        .group_by(Director.name)
        .order_by(func.sum(Movies.budget).desc())
        .all()
    )

    print(director[0][0])

    json_result = []

    for i in director:

        # nama = director_dict["name"] = i[0]
        # budget = director_dict["budget"] = i[1]
        json_result.append({"nama": i[0], "budget": i[1]})

    return jsonify(json_result)
