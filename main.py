from models import *
from flask import jsonify, render_template, request
from flask_restful import Api, Resource, abort, marshal_with, reqparse, fields
import time
from datetime import datetime, timedelta
import sqlite3
from functools import wraps
import jwt
import hashlib
import csv

# -------------Caching start--------
from config_flask_cache import *
app.config.from_mapping(config)
cache = Cache(app)
# --------Caching end---------------


# -------------JWT Token check START------------
app.config['SECRET_KEY'] = "thisissecret"


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if request.args['token']:
            token = request.args['token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], "HS256")
            global USER_ID
            USER_ID = data['USER_ID']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated
# -------jwt token check END-----------


# -------Root endpoint start-----------
@app.route("/")
@cache.cached(timeout=60)
def index():
    print("index function was called because data is not available as cache in redis database")
    return render_template("index.html")
# -------root endpoint end------------


# -------restful api start------
api = Api(app)
# -------restful api end--------


# -------Login start--------------
class Login(Resource):
    def post(self):
        format_user_login = reqparse.RequestParser()
        format_user_login.add_argument(
            "username", type=str, help="Username is required", required=True)
        format_user_login.add_argument(
            "password", type=str, help="Password is required", required=True)

        data = format_user_login.parse_args()
        # plain text to byte
        bp = hashlib.sha256(data['password'].encode())
        # convert to equivalent hexadecimal value
        password = bp.hexdigest()
        check_record = User.query.filter_by(
            username=data['username'], password=password).first()

        if check_record is None:
            abort(401, message="Wrong credentials")
        token = jwt.encode({'USER_ID': check_record.id, 'exp': datetime.utcnow(
        ) + timedelta(minutes=600)}, app.config['SECRET_KEY'])
        return {"token": token.decode('utf-8')}, 200


api.add_resource(Login, '/login')
# ------------Login end-------------

# ------User Registration start------


class Register(Resource):
    def post(self):

        format_user_register = reqparse.RequestParser()
        format_user_register.add_argument(
            "name", type=str, help="Name is required", required=True)
        format_user_register.add_argument(
            "email", type=str, help="Email is required", required=True)
        format_user_register.add_argument(
            "username", type=str, help="Username is required", required=True)
        format_user_register.add_argument(
            "password", type=str, help="Password is required", required=True)
        format_user_register.add_argument(
            "webhook_url", type=str, help="Webhook URL is required", required=True)

        data = format_user_register.parse_args()

        check_record_by_email = User.query.filter_by(
            email=data['email']).first()
        if check_record_by_email:
            abort(409, message="Email exists")

        check_record_by_username = User.query.filter_by(
            username=data['username']).first()
        if check_record_by_username:
            abort(409, message="Username exists")

        # plain text to byte
        bp = hashlib.sha256(data['password'].encode())
        # convert to equivalent hexadecimal value
        password = bp.hexdigest()

        new_user = User(
            username=data['username'], password=password, name=data['name'], email=data['email'], webhook_url=data['webhook_url'])
        db.session.add(new_user)
        db.session.commit()
        return {"message": "Registered successfully"}, 201


api.add_resource(Register, '/register')
# ------User Registration end------

# ----------Deck api start------------------

deck_output_format = {
    "id": fields.Integer,
    "name": fields.String,
    "average_score": fields.Integer,
    "last_review_time": fields.String,
    "user_id": fields.Integer
}


class DeckResource(Resource):
    @token_required
    @marshal_with(deck_output_format)
    def get(self):
        alldeck = Deck.query.filter_by(user_id=USER_ID).all()

        if len(alldeck) == 0:
            abort(403, message="You don't have a deck")
            # return {"message":"You don't have a deck"},403
        return alldeck

    @token_required
    @marshal_with(deck_output_format)
    def post(self):
        deck_input_format = reqparse.RequestParser()
        deck_input_format.add_argument(
            "name", type=str, help="Deck name is required", required=True)

        data = deck_input_format.parse_args()

        check_deck = Deck.query.filter_by(
            user_id=USER_ID, name=data['name']).first()
        if check_deck is None:
            new_deck = Deck(name=data['name'], user_id=USER_ID)
            db.session.add(new_deck)
            db.session.commit()
            return new_deck, 201
        else:
            abort(409, message="You already have this deck")
            # return {"message":"You already have this deck"},409

    @token_required
    @marshal_with(deck_output_format)
    def put(self):
        deck_input_format = reqparse.RequestParser()
        deck_input_format.add_argument(
            "id", type=int, help="Deck id is required", required=True)
        deck_input_format.add_argument(
            "name", type=str, help="Deck name is required", required=True)
        data = deck_input_format.parse_args()

        check_deck = Deck.query.filter_by(
            user_id=USER_ID, id=data['id']).first()

        if check_deck is None:
            abort(403, message="You don't have such a deck")
            # return {"message":"You don't have such a deck"},403

        check_deck.name = data['name']
        db.session.commit()
        return check_deck

    @token_required
    def delete(self):
        deck_input_format = reqparse.RequestParser()
        deck_input_format.add_argument(
            "id", type=int, help="Deck id is required", required=True)
        data = deck_input_format.parse_args()

        check_deck = Deck.query.filter_by(
            user_id=USER_ID, id=data['id']).first()

        if check_deck is None:
            abort(403, message="You don't have such a deck")
            # return {"message":"You don't have such a deck"},403

        db.session.delete(check_deck)
        db.session.commit()
        return {'message': 'Deck deleted'}


api.add_resource(DeckResource, '/deck')
# ----------DECK API END------------------

# ---------CARD API START-------------------
card_output_format = {
    "id": fields.Integer,
    "question": fields.String,
    "answer": fields.String,
    "last_review_time": fields.String,
    "score": fields.Integer,
    "deck_id": fields.Integer,
    "user_id": fields.Integer
}


class CardResource(Resource):
    @token_required
    @marshal_with(card_output_format)
    def get(self, deck_id):

        # ---- Check deck existence-----
        check_deck = Deck.query.filter_by(id=deck_id, user_id=USER_ID).first()
        if check_deck is None:
            abort(403, message="Deck doesn't exists")

        # ---- Check cards existence----
        if len(check_deck.cards) == 0:
            abort(403, message="No card in this deck")

        # ---- Return all cards of given deck----
        return check_deck.cards

    @token_required
    @marshal_with(card_output_format)
    def post(self, deck_id):

        # -----Card input json format ----
        card_input_format = reqparse.RequestParser()
        card_input_format.add_argument(
            "question", type=str, help="Question is required", required=True)
        card_input_format.add_argument(
            "answer", type=str, help="Answer is required", required=True)
        data = card_input_format.parse_args()

        # ----Check deck existence ----
        check_deck = Deck.query.filter_by(id=deck_id, user_id=USER_ID).first()
        if check_deck is None:
            abort(403, message="Sorry, Deck id not found")

        # ----Check card existence-----
        check_card = Card.query.filter_by(
            question=data['question'], deck_id=deck_id, user_id=USER_ID).first()
        if check_card is not None:
            abort(409, message="This card already exists")

        # ---- Create new card----
        new_card = Card(question=data['question'], answer=data['answer'],
                        last_review_time=0, next_review_time=0, score=0, deck_id=deck_id, user_id=USER_ID)
        db.session.add(new_card)
        db.session.commit()
        return new_card, 201

    @token_required
    @marshal_with(card_output_format)
    def put(self, deck_id):
        # ---- Card input json format
        card_input_format = reqparse.RequestParser()
        card_input_format.add_argument(
            "id", type=int, help="Card id is required", required=True)
        card_input_format.add_argument(
            "question", type=str, help="Question name is required", required=True)
        card_input_format.add_argument(
            "answer", type=str, help="Answer is required", required=True)
        card_input_format.add_argument(
            "last_review_time", type=int, help="Last review time", required=False)
        card_input_format.add_argument(
            "next_review_time", type=int, help="Next review time", required=False)
        card_input_format.add_argument(
            "score", type=int, help="Score of this card")
        data = card_input_format.parse_args()

        # ------check user existence-----
        check_user = User.query.filter_by(id=USER_ID).first()
        if check_user is None:
            abort(403, message="Sorry user doesn't exist")

        # ----Check deck existence ----
        check_deck = Deck.query.filter_by(id=deck_id, user_id=USER_ID).first()
        if check_deck is None:
            abort(403, message="Sorry, Deck id not found")

        # ---Check card existence
        check_card = Card.query.filter_by(
            id=data['id'], deck_id=deck_id, user_id=USER_ID).first()
        if check_card is None:
            abort(403, message="Sorry, card id not found")

        # ----Update card and deck----
        check_card.question = data['question']
        check_card.answer = data['answer']
        if data['last_review_time']:
            check_card.last_review_time = data['last_review_time']
            check_deck.last_review_time = data['last_review_time']
            check_user.last_review_time = data['last_review_time']
        if data['next_review_time']:
            check_card.next_review_time = data['next_review_time']
        if data['score']:
            current_score = check_card.score
            current_avg_deck_score = check_deck.average_score
            if current_avg_deck_score is None:
                current_avg_deck_score = 0
            total_card = len(check_deck.cards)
            print(total_card)
            new_avg_deck_score = (
                current_avg_deck_score*total_card - current_score + data['score'])/total_card
            check_card.score = data['score']
            check_deck.average_score = new_avg_deck_score
        db.session.commit()

        return check_card

    @token_required
    def delete(self, deck_id):
        card_input_format = reqparse.RequestParser()
        card_input_format.add_argument(
            "id", type=int, help="Card id is required", required=True)
        data = card_input_format.parse_args()

        # ----Check deck existence ----
        check_deck = Deck.query.filter_by(id=deck_id, user_id=USER_ID).first()
        if check_deck is None:
            abort(403, message="Sorry, Deck id not found")

        # ---Check card existence
        check_card = Card.query.filter_by(
            id=data['id'], deck_id=deck_id, user_id=USER_ID).first()
        if check_card is None:
            abort(403, message="Sorry, card id not found")

        # ----Delete card---
        db.session.delete(check_card)
        db.session.commit()
        return {'message': 'Card deleted'}


api.add_resource(CardResource, '/card/<int:deck_id>')

# ---------CARD API END-------------------

# ---------One card API at a time API START---------


class OneCardResource(Resource):
    @token_required
    @marshal_with(card_output_format)
    def get(self, deck_id):
        # ---- Check deck existence-----
        check_deck = Deck.query.filter_by(id=deck_id, user_id=USER_ID).first()
        if check_deck is None:
            abort(403, message="Deck doesn't exists")

        # ---- Check cards existence----
        if len(check_deck.cards) == 0:
            abort(403, message="No card in this deck")

        # ---- Select one card from given deck
        t = time.time()
        t = int(t*1000)  # timestamp in milliseconds
        conn = sqlite3.connect("project.sqlite")
        cur = conn.cursor()
        query = """SELECT id,question,answer,last_review_time,score,deck_id,user_id FROM card WHERE deck_id=? AND user_id=? AND next_review_time<? ORDER BY RANDOM() LIMIT 1"""
        cur.execute(query, (deck_id, USER_ID, t))
        row = cur.fetchone()
        if row is None:
            abort(404, message="No card left to review now! You can wait for some time")
        card_output_format = {
            "id": row[0],
            "question": row[1],
            "answer": row[2],
            "last_review_time": row[3],
            "score": row[4],
            "deck_id": row[5],
            "user_id": row[6]
        }
        # print(card_output_format)
        return card_output_format


api.add_resource(OneCardResource, "/onecard/<int:deck_id>")
# ---------One card at a time API END---------


# -----Import-Export Deck API START---------
class IEDeckResource(Resource):
    @token_required
    def get(self):
        check_user = User.query.filter_by(id=USER_ID).first()
        decks = check_user.decks
        if len(decks) == 0:
            abort(401, message="No deck found")
        # open the file in the write mode
        filename = "static/temp/"+str(USER_ID)+"-decks.csv"
        with open(filename, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            header = ['id', 'name', 'average_score',
                      'last_review_time', 'user_id']
            writer.writerow(header)

            # write multiple rows
            for deck in decks:
                d = [deck.id, deck.name, deck.average_score,
                     deck.last_review_time, deck.user_id]
                writer.writerow(d)
            link = "/"+filename
            return jsonify({"link": link})


api.add_resource(IEDeckResource, "/iedeck")
# -----Import-Export Deck API END---------


# -----Import-Export API Card START---------
class IECardResource(Resource):
    @token_required
    def get(self):
        check_user = User.query.filter_by(id=USER_ID).first()
        cards = check_user.cards
        if len(cards) == 0:
            abort(401, message="No Card found")
        # open the file in the write mode
        filename = "static/temp/"+str(USER_ID)+"-cards.csv"
        with open(filename, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            header = ['id', 'question', 'answer', 'last_review_time',
                      'next_review_time', 'score', 'deck_id', 'user_id']
            writer.writerow(header)

            # write multiple rows
            for card in cards:
                d = [card.id, card.question, card.answer, card.last_review_time,
                     card.next_review_time, card.score, card.deck_id, card.user_id]
                writer.writerow(d)
            link = "/"+filename
            return jsonify({"link": link})


api.add_resource(IECardResource, "/iecard")

if __name__ == '__main__':
    app.run(debug=True)
