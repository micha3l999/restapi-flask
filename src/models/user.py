from datetime import datetime
from .instance import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    bookmarks = db.relationship('Bookmark', backref="user")

    # Return a represetation of the class
    def __repr__(self) -> str:
        return f'User: {self.username}'
