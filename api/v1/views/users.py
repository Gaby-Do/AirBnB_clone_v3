#!/usr/bin/python3
"""City, RESTful API methods"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User


@app_views.route('/users',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def user_all():
    """Returns a json with all the cities of a state"""
    if request.method == 'GET':
        user_list = storage.all(User)
        response = []
        for key, value in user_list.items():
            response.append(value.to_dict())
        return jsonify(response)

    if request.method == 'POST':
        if not request.is_json:
            abort(400, 'Not a JSON')

        content = request.get_json(force=True)
        if content is None:
            abort(400, "Not a JSON")
        if 'email' not in content.keys():
            abort(400, 'Missing email')
        if 'password' not in content.keys():
            abort(400, 'Missing password')
        new_user = User(**content)
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user_get(user_id):
    """Returns a json of a given City"""
    my_user = storage.get(User, user_id)
    if my_user is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(my_user.to_dict())

    if request.method == 'DELETE':
        my_user.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.is_json:
            abort(400, 'Not a JSON')
        ignore = ["id", "email", "created_at", "updated_at"]
        content = request.get_json(force=True)
        if content is None:
            abort(400, "Not a JSON")
        for key, value in content.items():
            if key not in ignore:
                setattr(my_user, key, value)
        storage.save()
        return jsonify(my_user.to_dict()), 200
