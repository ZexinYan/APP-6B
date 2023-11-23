from bson.objectid import ObjectId
from flask_restful import Resource, reqparse
from database.player import PlayerTable
from database.bank_account import BankAccountTable
from database.request import RequestTable
from utils.response import response

player_table = PlayerTable()
bank_account_table = BankAccountTable()
request_table = RequestTable()


class Player(Resource):
    def get(self, ID=None):
        if ID is None:
            user_list = player_table.find()
            for idx in range(len(user_list)):
                del user_list[idx]['password']
            return response(status=200, message={'user_info': user_list})
        else:
            user_list = player_table.find(condition={'_id': ObjectId(ID)})
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
            player_table.insert_one({
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
            player_table.delete_one(ID)
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
            player_table.update_one(ID, update_info)
            return response(status=200)
        except Exception as _:
            return response(status=401, message='Invalid user information.')


class BankAccount(Resource):
    def get(self, player_id, account_id=None):
        if account_id is None:
            bank_account_list = bank_account_table.find(condition={'user_id': player_id})
            return response(status=200, message={'bank_account_list': bank_account_list})
        else:
            bank_account_list = bank_account_table.find(condition={'_id': ObjectId(account_id)})
            if len(bank_account_list) == 1:
                return response(status=200, message={'bank_account': bank_account_list[0]})
            else:
                return response(status=401, message='Invalid request.')

    def post(self, player_id):
        parser = reqparse.RequestParser()
        parser.add_argument('holder_name', type=str, required=True)
        parser.add_argument('account_number', type=str, required=True)
        parser.add_argument('bank_name', type=str, required=True)
        args = parser.parse_args()
        try:
            bank_account_table.insert_one({
                'user_id': player_id,
                'holder_name': args.holder_name,
                'account_number': args.account_number,
                'bank_name': args.bank_name
            })
            return response(status=200)
        except Exception as _:
            return response(status=401, message='Invalid bank account information.')

    def delete(self, player_id, account_id):
        try:
            bank_account_info = bank_account_table.find(condition={'_id': ObjectId(account_id)})[0]
            if bank_account_info['user_id'] != player_id:
                raise Exception
            bank_account_table.delete_one(account_id)
            return response(status=200)
        except Exception as _:
            return response(status=401, message='Invalid request.')

    def put(self, player_id, account_id):
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

