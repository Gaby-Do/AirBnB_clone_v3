#!/usr/bin/python3
"""City, RESTful API methods"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route('/amenities',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def ameni_all():
    """Returns a json with all the cities of a state"""
    if request.method == 'GET':
        ameni_list = storage.all(Amenity)
        response = []
        for key, value in ameni_list.items():
            response.append(value.to_dict())
        return jsonify(response)

    if request.method == 'POST':
        if not request.is_json:
            abort(400, 'Not a JSON')

        content = request.get_json(force=True)
        if content is None:
            abort(400, "Not a JSON")
        if 'name' not in content.keys():
            abort(400, 'Missing name')
        new_amenity = Amenity(**content)
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def ameni_get(amenity_id):
    """Returns a json of a given City"""
    my_amenity = storage.get(Amenity, amenity_id)
    if my_amenity is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(my_amenity.to_dict())

    if request.method == 'DELETE':
        my_amenity.delete()
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
                setattr(my_amenity, key, value)
        storage.save()
        return jsonify(my_amenity.to_dict()), 200
