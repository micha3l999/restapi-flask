from flask import Blueprint

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post('/register')
def register_user():
    return "User registered"


@auth.get('/get-user/<string:username>')
def get_user(username):
    return f"User: {username}"
