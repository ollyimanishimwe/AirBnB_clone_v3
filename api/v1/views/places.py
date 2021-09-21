#!/usr/bin/python3
""" Place view
"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def get_place(place_id=None):
    """ Fetches place object if exists
    """
    if place_id is not None:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        return jsonify(place.to_dict())
    abort(404)


@app_views.route("/cities/<city_id>/places", methods=['GET'], strict_slashes=False)
def get_places(city_id=None):
    """ Fetches place objects in a state
    """
    if city_id is not None:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        places = list(map(lambda obj: obj.to_dict(), city.places))
        return jsonify(places)
    abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'], strict_slashes=False)
def delete_place(place_id=None):
    """ Deletes a place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=['POST'], strict_slashes=False)
def insert_place(city_id=None):
    """ Creates a new place object
    """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    req_data = request.get_json()
    if "name" not in req_data.keys():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    if "user_id" not in req_data.keys():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get(User, req_data.user_id)
    city = storage.get(City, city_id)
    if city is None or user is None:
        abort(404)
    req_data.update({"city_id": city.id})
    new_place = Place(**req_data)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route("/places/<place_id>",methods=['PUT'], strict_slashes=False)
def update_place(place_id=None):
    """ Updates a place with request data
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    req_data = request.get_json()
    req_data.pop("id", None)
    req_data.pop("created_at", None)
    req_data.pop("updated_at", None)
    [setattr(place, k, v) for k, v in req_data.items()]
    place.save()
    return make_response(jsonify(place.to_dict()), 200)
