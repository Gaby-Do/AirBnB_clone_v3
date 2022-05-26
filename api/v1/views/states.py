#!/usr/bin/python3
"""4. Status of your API"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.route('/states',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def states_all():
    """Returns a json with all the states in the system"""
    if request.method == 'GET':
        state_list = storage.all(State)
        response = []
        for key, value in state_list.items():
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
        new_state = State(**content)
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def states_get(state_id):
    """Returns a json of a given State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(state.to_dict())

    if request.method == 'DELETE':
        state.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.is_json:
            abort(400, 'Not a JSON')
        ignore = ["id", "created_at", "updated_at"]
        content = request.get_json(force=True)
        if content is None:
            abort(400, "Not a JSON")
        for key, value in content.items():
            if key not in ignore:
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict()), 200
