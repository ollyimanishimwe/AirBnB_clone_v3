#!/usr/bin/python3
""" Reviews view
"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def get_review(review_id=None):
    """ Fetches review object if exists
    """
    if review_id is not None:
        review = storage.get(Review, review_id)
        if review is None:
            abort(404)
        return jsonify(review.to_dict())
    abort(404)


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id=None):
    """ Fetches review objects in a state
    """
    if place_id is not None:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        reviews = list(map(lambda obj: obj.to_dict(), place.reviews))
        return jsonify(reviews)
    abort(404)


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    """ Deletes a review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def insert_review(place_id=None):
    """ Creates a new review object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    req_data = request.get_json()
    if "text" not in req_data.keys():
        return make_response(jsonify({'error': 'Missing text'}), 400)
    if "user_id" not in req_data.keys():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)

    user = storage.get(User, req_data.user_id)
    if user is None:
        abort(404)
    req_data.update({"place_id": place.id})
    new_review = Review(**req_data)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=['PUT'], strict_slashes=False)
def update_review(review_id=None):
    """ Updates a review with request data
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    req_data = request.get_json()
    req_data.pop("id", None)
    req_data.pop("created_at", None)
    req_data.pop("updated_at", None)
    [setattr(review, k, v) for k, v in req_data.items()]
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
