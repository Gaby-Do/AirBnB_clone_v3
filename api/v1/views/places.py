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


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def places_all(city_id):
    """Returns a json with all the places of a city"""
    if storage.get(City, city_id) is None:
        abort(404)
    if request.method == 'GET':
        places_list = storage.all(Place)
        response = []
        for key, value in places_list.items():
            if (value.city_id == city_id):
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
        if 'name' not in content.keys():
            abort(400, 'Missing name')

        content['city_id'] = city_id
        new_place = Place(**content)
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_get(place_id):
    """Returns a json of a given Place"""
    my_place = storage.get(Place, place_id)
    if my_place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(my_place.to_dict())

    if request.method == 'DELETE':
        my_place.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        ignore = ["id", "user_id", "city_id", "created_at", "updated_at"]
        content = request.get_json(force=True)
        if content is None:
            abort(400, "Not a JSON")
        for key, value in content.items():
            if key not in ignore:
                setattr(my_place, key, value)
        storage.save()
        return jsonify(my_place.to_dict()), 200
