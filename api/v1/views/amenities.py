#!/usr/bin/python3
""" Amenity view
"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_amenities(amenity_id=None):
    """ Fetches amenity objects or one amenity object if exists
    """
    if amenity_id is not None:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        else:
            return jsonify(amenity.to_dict())
    objs = list(map(lambda obj: obj.to_dict(), storage.all(Amenity).values()))
    return jsonify(objs)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    """ Deletes an amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def insert_amenity():
    """ Creates a new amenity object
    """
    req_data = {}
    try:
        req_data = request.get_json()
    except Exception:
        make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "name" not in req_data.keys():
        make_response(jsonify({'error': 'Missing name'}), 400)
    new_amenity = Amenity(**req_data)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id=None):
    """ Updates amenity with request data
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    req_data = {}
    try:
        req_data = request.get_json()
    except Exception:
        make_response(jsonify({'error': 'Not a JSON'}), 400)
    req_data.pop("id", None)
    req_data.pop("created_at", None)
    req_data.pop("updated_at", None)
    [setattr(amenity, k, v) for k, v in req_data.items()]
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
