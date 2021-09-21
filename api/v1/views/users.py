#!/usr/bin/python3
""" User view
"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=['GET'], strict_slashes=False)
@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def get_users(user_id=None):
    """ Fetches user objects or one user object if exists
    """
    if user_id is not None:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        else:
            return jsonify(user.to_dict())
    objs = list(map(lambda obj: obj.to_dict(), storage.all(User).values()))
    return jsonify(objs)


@app_views.route("/users/<user_id>", methods=['DELETE'], strict_slashes=False)
def delete_user(user_id=None):
    """ Deletes a user object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def insert_user():
    """ Creates a new user object
    """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    req_data = request.get_json()
    if "email" not in req_data.keys():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if "password" not in req_data.keys():
        return make_response(jsonify({'error': 'Missing password'}), 400)
    new_user = User(**req_data)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id=None):
    """ Updates a user object with request data
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    req_data = request.get_json()
    req_data.pop("id", None)
    req_data.pop("created_at", None)
    req_data.pop("updated_at", None)
    [setattr(user, k, v) for k, v in req_data.items()]
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
