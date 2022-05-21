from flask import Blueprint, jsonify, request
import validators
from operator import itemgetter
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.models.bookmark import Bookmark
from src.models.instance import db
from src.constants.status_codes import HTTP_200_SUCCESS, HTTP_400_BAD_REQUEST

bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")


@bookmarks.route("/", methods=["GET", "POST"])
@jwt_required()
def get_all():

    # Get the user id from the token
    user_id = get_jwt_identity()

    # Manage the post request
    if request.method == "POST":

        request_data = request.get_json()

        body = request_data.get("body", "")
        url = request_data.get("url", "")
        visits = request_data.get("visits", "")

        # Check required parameters
        if not body:
            return jsonify({
                "error": "The body is required"
            }), HTTP_400_BAD_REQUEST

        if not url:
            return jsonify({
                "error": "The url is required"
            }), HTTP_400_BAD_REQUEST

        if not visits:
            return jsonify({
                "error": "The visits is required"
            }), HTTP_400_BAD_REQUEST

        if not validators.url(url):
            return jsonify({
                "error": "The url is not valid"
            }), HTTP_400_BAD_REQUEST

        bookmark = Bookmark(body=body, url=url, visits=visits, user_id=user_id)
        db.session.add(bookmark)
        db.session.commit()

        return jsonify({
            "message": "Bookmark created successfully",
            "bookmark": {
                "id": bookmark.id,
                "url": bookmark.url,
                "short_url": bookmark.short_url,
                "visits": bookmark.visits,
            }
        }), HTTP_200_SUCCESS
    else:

        # Search the bookmarks of the user
        bookmarks = Bookmark.query.filter_by(user_id=user_id)

        data = []
        for bookmark in bookmarks:
            data.append({
                "id": bookmark.id,
                "body": bookmark.body,
                "url": bookmark.url,
                "short_url": bookmark.short_url,
                "visits": bookmark.visits,

            })
        return jsonify({
            "message": "All records retrieve successfully",
            "data": data,
        }), HTTP_200_SUCCESS
