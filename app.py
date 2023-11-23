import argparse
from flask import Flask, Response
from flask_restful import Api, Resource, reqparse
from resource.player import Player, BankAccount as PlayerBankAccount
from resource.organizer import Organizer, OrganizerBankAccount, OrganizerEvent
from resource.rating import Rating, Comment

app = Flask(__name__)
api = Api(app)
db = None

api.add_resource(Player, '/api/player', '/api/player/<ID>')
api.add_resource(PlayerBankAccount,
                 '/api/player/<string:player_id>/bank_account',
                 '/api/player/<string:player_id>/bank_account/<string:account_id>')
api.add_resource(Organizer, '/api/organizer', '/api/organizer/<ID>')
api.add_resource(OrganizerBankAccount,
                 '/api/organizer/<string:organizer_id>/bank_account',
                 '/api/organizer/<string:organizer_id>/bank_account/<string:account_id>')
api.add_resource(OrganizerEvent,
                 '/api/organizer/<string:organizer_id>/event',
                 '/api/organizer/<string:organizer_id>/event/<string:event_id>')
api.add_resource(Rating,
                 '/api/rating',
                 '/api/rating/<ID>')
api.add_resource(Comment,
                 '/api/rating/<string:rating_id>/comment',
                 '/api/rating/<string:rating_id>/comment/<string:comment_id>')


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
