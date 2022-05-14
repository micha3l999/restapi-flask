from datetime import datetime
import random
import string
from .instance import db


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    url = db.Column(db.Text, nullable=False)
    short_url = db.Column(db.String(50))
    visits = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())

    updated_at = db.Column(db.DateTime, default=datetime)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.short_url = self.generate_short_characters()

    def generate_short_characters(self):
        characters = string.digits + string.ascii_letters
        picked_chars = ''.join(random.choices(characters, k=5))

        # Search if there's any match with the short_url generated
        link = self.query.filter_by(short_url=picked_chars).first()

        if link:
            self.generate_short_characters()
        else:
            return picked_chars

    # Return a represetation of the class
    def __repr__(self) -> str:
        return f"Bookmark: {self.url}"
