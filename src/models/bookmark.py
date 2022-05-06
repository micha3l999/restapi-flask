import datetime
from database import db


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    url = db.Column(db.Text, nullable=False)
    short_url = db.Column(db.String(50))
    visits = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.Datetime, default=datetime.now())
    updated_at = db.Column(db.Datetime, default=datetime.now())

    def __repr__(self) -> str:
        return f"Bookmark: {self.url}"
