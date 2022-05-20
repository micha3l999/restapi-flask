from os import access
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import validators
from flask_jwt_extended import create_access_token, jwt_required, create_refresh_token, get_jwt_identity
from src.models.user import User, db

from src.constants.status_codes import HTTP_200_SUCCESS, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post('/register')
def register_user():
    # Read data from the request
    request_data = request.get_json()

    if not request_data:
        return jsonify({
            "message": "The body must not be empty",
        }), HTTP_400_BAD_REQUEST

    email = request_data.get("email")
    username = request_data.get("username")
    password = request_data.get('password')

    # Check if parameters exists or follow the policies
    if not 'email' or not 'username' or not 'password' in request_data:
        return jsonify({
            "message": "You need to send more parameters",
        }), HTTP_400_BAD_REQUEST

    # Check if password is less than 5 characters
    if len(password) < 5:
        return jsonify({
            "error": "The password need to be longer",
        }), HTTP_400_BAD_REQUEST

    # Check if username is less than 3 characters
    if len(username) < 3:
        return jsonify({
            "error": "The username is too short",
        }), HTTP_400_BAD_REQUEST

    # Validate the email format
    if not validators.email(email):
        return jsonify({
            "error": "The email is not valid"
        }), HTTP_400_BAD_REQUEST

    # Check if username is alphanumeric
    if not username.isalnum() or " " in username:
        return jsonify({
            "error": "The username should be alphanumeric ",
        }), HTTP_400_BAD_REQUEST

    # Check if the user already exists
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({
            "error": "The user already exists ",
        }), HTTP_409_CONFLICT

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({
            "error": "The user already exists ",
        }), HTTP_409_CONFLICT

    # Generate hash password
    encrypted_password = generate_password_hash(password)

    # Create and save the user
    user = User(username=username, email=email, password=encrypted_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User created",
        "data": {
            "user": {
                "email": email,
                "username": username,
            }
        }
    })


@auth.put('/login')
def login_user():
    request_data = request.get_json()

    email = request_data.get("email")
    password = request_data.get("password")

    # Validate required fields
    if not email:
        return jsonify({
            "message": "the email is required",
        })
    if not password:
        return jsonify({
            "message": "the password is required",
        })

    # Query and check passwords
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "message": "The user does not exists"
        }), HTTP_409_CONFLICT

    password_checking = check_password_hash(user.password, password)

    if not password_checking:
        return jsonify({
            "message": "The password is not correct"
        }), HTTP_409_CONFLICT

    access = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        "message": "Login successfull",
        "data": {
            "user": {
                "access": access,
                "refresh": refresh_token,
                "username": user.username,
                "email": user.email
            }
        }
    }), HTTP_200_SUCCESS


@auth.get('/get-user')
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "message": "User information successfully retrieved",
        "user": {
            "email": user.email,
            "created_at": user.created_at,
            "username": user.username,
        },
    }), HTTP_200_SUCCESS
