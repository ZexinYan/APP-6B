from bson.objectid import ObjectId
from flask_restful import Resource, reqparse
from database.rating import RatingTable
from database.comment import CommentTable
from utils.response import response

rating_table = RatingTable()
comment_table = CommentTable()


class Rating(Resource):
    def get(self, ID=None):
        if ID is None:
            rating_list = rating_table.find()
            return response(status=200, message={'rating_list': rating_list})
        else:
            rating_list = rating_table.find(condition={'_id': ObjectId(ID)})
            if len(rating_list) == 1:
                return response(status=200, message={'rating': rating_list[0]})
            else:
                return response(status=401, message='Invalid request.')

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('rater', type=str, required=True)
        parser.add_argument('time', type=str, required=True)
        parser.add_argument('event', type=str, required=True)
        args = parser.parse_args()
        try:
            rating_table.insert_one({
                'rater': args.rater,
                'time': args.time,
                'event': args.event
            })
            return response(status=200)
        except Exception as _:
            return response(status=401, message='Invalid request.')

    def delete(self, ID):
        try:
            rating_table.delete_one(ID)
            return response(status=200)
        except Exception as _:
            return response(status=401, message='Invalid request.')


class Comment(Resource):
    def get(self, rating_id, comment_id=None):
        if comment_id is None:
            comment_list = comment_table.find(condition={'rating': rating_id})
            return response(status=200, message={'comments': comment_list})
        else:
            comment_list = comment_table.find(condition={'_id': ObjectId(comment_id)})
            if len(comment_list) == 1:
                return response(status=200, message={'comments': comment_list[0]})
            else:
                return response(status=401, message='Invalid request.')

    def post(self, rating_id):
        parser = reqparse.RequestParser()
        parser.add_argument('content', type=str, required=True)
        args = parser.parse_args()
        try:
            comment_table.insert_one({
                'rating': rating_id,
                'content': args.content
            })
            return response(status=200)
        except Exception as _:
            return response(status=401, message='Invalid request.')

    def put(self, rating_id, comment_id):
        parser = reqparse.RequestParser()
        parser.add_argument('content', type=str, required=True)
        args = parser.parse_args()
        try:

            comment_table.update_one(comment_id, {
                'content': args.content
            })
            return response(status=200)
        except Exception as _:
            return response(status=401, message='Invalid request.')

    def delete(self, rating_id, comment_id):
        try:
            comment_table.delete_one(comment_id)
            return response(status=200)
        except Exception as _:
            return response(status=401, message='Invalid request.')
