# from email import message
# import json
# from flask import Flask
# from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# api = Api(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# db = SQLAlchemy(app)


# class BookModel(db.Model):
#     id_book = db.Column(db.Integer, primary_key=True)
#     title_book = db.Column(db.String(25), nullable=False)

#     def __repr__(self) -> str:
#         return f"Book(name = {self.title_book}, id= {self.id_book})"


# books_args = reqparse.RequestParser(bundle_errors=True)
# books_args.add_argument(
#     "title", type=str, help="The error is {error_msg}", required=True)
# books_args.add_argument("autor", type=str, help="the autor is needed")
# books_args.add_argument("qualification", type=int,
#                         choices=(1, 2, 3), required=True)

# resource_fields = {
#     "book_id": fields.Integer,
#     "book_title": fields.String,
# }

# books = {}


# def check_book(book_id):
#     if book_id in books:
#         abort(409, message="The book already exists")


# def check_not_book(book_id):
#     if book_id not in books:
#         abort(409, message="The book doesn't exist")


# class Book(Resource):
#     def get(self, book_id):
#         check_not_book(book_id)
#         return books[book_id], 200

#     @marshal_with(resource_fields)
#     def put(self, book_id):
#         args = books_args.parse_args()
#         result = BookModel.query.filter_by(book_id=book_id).first()
#         if not result:
#             abort(404, message="The book doesn't exist")
#         return result

#     def post(self, book_id):
#         check_book(book_id)
#         args = books_args.parse_args()
#         books[book_id] = args

#         return json.dumps({
#             "message": "the post was done",
#             "data": books,
#         }), 201

#     def delete(self, book_id):
#         check_not_book(book_id)
#         del books[book_id]
#         return {
#             "message": "The record was deleted",
#         }, 200


# api.add_resource(Book, "/books/<int:book_id>")


# class Books(Resource):
#     def get(self):
#         return books


# api.add_resource(Books, "/books")


# class HiMom(Resource):
#     def put(self):
#         return {
#             "data": "the update was done",
#             "status": "200"
#         }

#     def get(self, message):
#         return f"<h1>hola si si si{message}</h1>"


# api.add_resource(HiMom, "/himom/<string:message>")


# @app.get("/hello")
# def index():
#     return "<h1>hello</h1>"


# if __name__ == "__main__":
#     app.run(debug=True, port=3000)
