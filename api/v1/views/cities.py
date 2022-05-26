#!/usr/bin/python3
"""City, RESTful API methods"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def city_all(state_id):
    """Returns a json with all the cities of a state"""
    if request.method == 'GET':
        if storage.get(State, state_id) is None:
            abort(404)
        city_list = storage.all(City)
        # print("state id: {}".format(state_id))
        # print(city_list)
        response = []
        for key, value in city_list.items():
            if value.state_id == state_id:
                response.append(value.to_dict())
        return jsonify(response)

    if request.method == 'POST':
        if storage.get(State, state_id) is None:
            abort(404)
        if not request.is_json:
            abort(400, 'Not a JSON')

        content = request.get_json(force=True)
        if content is None:
            abort(400, "Not a JSON")
        if 'name' not in content.keys():
            abort(400, 'Missing name')
        content['state_id'] = state_id
        new_city = City(**content)
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def city_get(city_id):
    """Returns a json of a given City"""
    my_city = storage.get(City, city_id)
    if my_city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(my_city.to_dict())

    if request.method == 'DELETE':
        my_city.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.is_json:
            abort(400, 'Not a JSON')
        ignore = ["id", "state_id", "created_at", "updated_at"]
        content = request.get_json(force=True)
        if content is None:
            abort(400, "Not a JSON")
        for key, value in content.items():
            if key not in ignore:
                setattr(my_city, key, value)
        storage.save()
        return jsonify(my_city.to_dict()), 200
