#!/usr/bin/python3
""" City view
"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city(city_id=None):
    """ Fetches city object if exists
    """
    if city_id is not None:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        return jsonify(city.to_dict())
    abort(404)


@app_views.route("/states/<state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id=None):
    """ Fetches city objects in a state
    """
    if state_id is not None:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        cities = list(map(lambda obj: obj.to_dict(), state.cities))
        return jsonify(cities)
    abort(404)


@app_views.route("/cities/<city_id>", methods=['DELETE'], strict_slashes=False)
def delete_city(city_id=None):
    """ Deletes a city object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def insert_city(state_id=None):
    """ Creates a new city object
    """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    req_data = request.get_json()
    if "name" not in req_data.keys():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    req_data.update({"state_id": state.id})
    new_city = City(**req_data)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route("cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city(city_id=None):
    """ Updates a city with request data
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    req_data = request.get_json()
    req_data.pop("id", None)
    req_data.pop("created_at", None)
    req_data.pop("updated_at", None)
    [setattr(city, k, v) for k, v in req_data.items()]
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
