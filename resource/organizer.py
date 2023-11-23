from flask import request
from bson.objectid import ObjectId
from flask_restful import Resource, reqparse
from database.organizer import OrganizerTable
from database.bank_account import BankAccountTable
from database.event import EventTable
from utils.response import response

organizer_table = OrganizerTable()
bank_account_table = BankAccountTable()
event_table = EventTable()


class Organizer(Resource):
    def get(self, ID=None):
        if ID is None:
            user_list = organizer_table.find()
            for idx in range(len(user_list)):
                del user_list[idx]['password']
            return response(status=200, message={'user_info': user_list})
        else:
            user_list = organizer_table.find(condition={'_id': ObjectId(ID)})
            if len(user_list) != 1:
                return response(status=401, message='Invalid user.')
            else:
                user_info = user_list[0]
                del user_info['password']
                return response(status=200, message={'user_info': user_info})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        parser.add_argument('address', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('phone', type=str, required=True)
        args = parser.parse_args()
        try:
            organizer_table.insert_one({
                'first_name': args.first_name,
                'last_name': args.last_name,
                'address': args.address,
                'password': args.password,
                'phone': args.phone,
                'email': args.email
            })
            return response(status=200)
        except Exception as _:
            return response(status=401, message='Invalid user information.')

    def delete(self, ID):
        try:
            organizer_table.delete_one(ID)
            return response(status=200)
        except Exception as _:
            return response(status=401, message='Invalid request.')

    def put(self, ID):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=False, default=None)
        parser.add_argument('last_name', type=str, required=False, default=None)
        parser.add_argument('address', type=str, required=False, default=None)
        parser.add_argument('password', type=str, required=False, default=None)
        parser.add_argument('email', type=str, required=False, default=None)
        parser.add_argument('phone', type=str, required=False, default=None)
        args = parser.parse_args()
        try:
            update_info = {}
            for key in args:
                if args[key] is not None:
                    update_info[key] = args[key]
            organizer_table.update_one(ID, update_info)
            return response(status=200)
        except Exception as _:
            return response(status=401, message='Invalid user information.')


class OrganizerBankAccount(Resource):
    def get(self, organizer_id, account_id=None):
        if account_id is None:
            bank_account_list = bank_account_table.find(condition={'user_id': organizer_id})
            return response(status=200, message={'bank_account_list': bank_account_list})
        else:
            bank_account_list = bank_account_table.find(condition={'_id': ObjectId(account_id)})
            if len(bank_account_list) == 1:
                return response(status=200, message={'bank_account': bank_account_list[0]})
            else:
                return response(status=401, message='Invalid request.')

    def post(self, organizer_id):
        parser = reqparse.RequestParser()
        parser.add_argument('holder_name', type=str, required=True)
        parser.add_argument('account_number', type=str, required=True)
        parser.add_argument('bank_name', type=str, required=True)
        args = parser.parse_args()
        try:
            bank_account_table.insert_one({
                'user_id': organizer_id,
                'holder_name': args.holder_name,
                'account_number': args.account_number,
                'bank_name': args.bank_name
            })
            return response(status=200)
        except Exception as _:
            return response(status=401, message='Invalid bank account information.')

    def delete(self, organizer_id, account_id):
        try:
            bank_account_info = bank_account_table.find(condition={'_id': ObjectId(account_id)})[0]
            if bank_account_info['user_id'] != organizer_id:
                raise Exception
            bank_account_table.delete_one(account_id)
            return response(status=200)
        except Exception as _:
            return response(status=401, message='Invalid request.')

    def put(self, organizer_id, account_id):
        parser = reqparse.RequestParser()
        parser.add_argument('holder_name', type=str, required=False, default=None)
        parser.add_argument('account_number', type=str, required=False, default=None)
        parser.add_argument('bank_name', type=str, required=False, default=None)
        args = parser.parse_args()
        try:
            update_info = {}
            for key in args:
                if args[key] is not None:
                    update_info[key] = args[key]
            bank_account_table.update_one(account_id, update_info)
            return response(status=200)
        except Exception as _:
            return response(status=401, message='Invalid request.')


class OrganizerEvent(Resource):
    def get(self, organizer_id, event_id=None):
        category = request.args.get('category', None)
        sortby = request.args.get('sortby', None)
        begin = request.args.get('begin', None)
        count = request.args.get('count', None)
        condition = {
            'organizer_id': organizer_id
        }
        if category is not None:
            condition['category'] = category
        if begin is not None:
            begin = int(begin)
        if count is not None:
            count = int(count)
        if event_id is None:
            event_list = event_table.find(condition=condition,
                                          sort={'key': sortby, 'value': 1} if sortby is not None else None,
                                          skip=begin, limit=count)
            return response(status=200, message={'event_list': event_list})
        else:
            condition['_id'] = ObjectId(event_id)
            event_list = event_table.find(condition=condition,
                                          sort={'key': sortby, 'value': -1} if sortby is not None else None,
                                          skip=begin, limit=count)
            if len(event_list) == 1:
                return response(status=200, message={'event': event_list[0]})
            else:
                return response(status=401, message='Invalid request.')

    def post(self, organizer_id):
        parser = reqparse.RequestParser()
        parser.add_argument('time', type=str, required=True)
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('desc', type=str, required=True)
        parser.add_argument('location', type=str, required=True)
        parser.add_argument('category', type=str, required=True)
        args = parser.parse_args()
        try:
            event_table.insert_one({
                'organizer_id': organizer_id,
                'time': args.time,
                'name': args.name,
                'desc': args.desc,
                'category': args.category
            })
            return response(status=200)
        except Exception as _:
            return response(status=401, message='Invalid event creation.')

    def delete(self, organizer_id, event_id):
        try:
            event_list = event_table.find(condition={
                '_id': ObjectId(event_id),
                'organizer_id': organizer_id
            })
            if len(event_list) == 1:
                event_table.delete_one(event_id)
                return response(status=200)
        except Exception as _:
            return response(status=401, message='Invalid request.')

    def put(self, organizer_id, event_id):
        parser = reqparse.RequestParser()
        parser.add_argument('time', type=str, required=False, default=None)
        parser.add_argument('name', type=str, required=False, default=None)
        parser.add_argument('location', type=str, required=False, default=None)
        parser.add_argument('desc', type=str, required=False, default=None)
        parser.add_argument('category', type=str, required=False, default=None)
        args = parser.parse_args()
        try:
            update_info = {}
            for key in args:
                if args[key] is not None:
                    update_info[key] = args[key]
            event_table.update_one(event_id, update_info)
            return response(status=200)
        except Exception as _:
            return response(status=401, message='Invalid request.')

