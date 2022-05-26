#!/usr/bin/python3
"""City, RESTful API methods"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def rev_all(place_id):
    """Returns a json with all the reviews for a places"""
    if storage.get(Place, place_id) is None:
        abort(404)
    if request.method == 'GET':
        rev_list = storage.all(Review)
        response = []
        for key, value in rev_list.items():
            if (value.place_id == place_id):
                response.append(value.to_dict())
        return jsonify(response)

    if request.method == 'POST':
        content = request.get_json(force=True)
        if content is None:
            abort(400, "Not a JSON")

        if 'user_id' not in content.keys():
            abort(400, 'Missing user_id')
        if storage.get(User, content['user_id']) is None:
            abort(404)
        if 'text' not in content.keys():
            abort(400, 'Missing text')

        content['place_id'] = place_id
        new_rev = Review(**content)
        storage.new(new_rev)
        storage.save()
        return jsonify(new_rev.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def rev_get(review_id):
    """Returns a json of a given Place"""
    my_rev = storage.get(Review, review_id)
    if my_rev is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(my_rev.to_dict())

    if request.method == 'DELETE':
        my_rev.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
        content = request.get_json(force=True)
        if content is None:
            abort(400, "Not a JSON")
        for key, value in content.items():
            if key not in ignore:
                setattr(my_rev, key, value)
        storage.save()
        return jsonify(my_rev.to_dict()), 200
