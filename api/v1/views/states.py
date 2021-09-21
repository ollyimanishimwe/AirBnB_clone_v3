#!/usr/bin/python3
""" State view
"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    """ Fetches state objects or one state object if exists
    """
    if state_id is not None:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        else:
            return jsonify(state.to_dict())
    objs = list(map(lambda obj: obj.to_dict(), storage.all(State).values()))
    return jsonify(objs)


@app_views.route("/states/<state_id>", methods=['DELETE'], strict_slashes=False)
def delete_state(state_id=None):
    """ Deletes a state object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def insert_state():
    """ Creates a new state object
    """
    req_data = {}
    try:
        req_data = request.get_json()
    except Exception:
        make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "name" not in req_data.keys():
        make_response(jsonify({'error': 'Missing name'}), 400)
    new_state = State(**req_data)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route("/states/<state_id>",methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    """ Updates a state with request data
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    req_data = {}
    try:
        req_data = request.get_json()
    except Exception:
        make_response(jsonify({'error': 'Not a JSON'}), 400)
    req_data.pop("id", None)
    req_data.pop("created_at", None)
    req_data.pop("updated_at", None)
    [setattr(state, k, v) for k, v in req_data.items()]
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
