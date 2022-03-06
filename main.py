from models import *
from flask import jsonify, render_template, request
from datetime import datetime,timedelta





import jwt
from functools import wraps

def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
      token = None

      if request.args['token']:
          token = request.args['token']

      if not token:
          return jsonify({'message' : 'Token is missing!'}), 401

      try: 
          data = jwt.decode(token, app.config['SECRET_KEY'],"HS256")
          global USER_ID
          USER_ID=data['USER_ID']
      except:
          return jsonify({'message' : 'Token is invalid!'}), 401

      return f( *args, **kwargs)

  return decorated











@app.route("/")
def index():
    return render_template("index.html")
















from flask_restful import Api, Resource, abort, marshal_with,reqparse,fields
api=Api(app)





#-------Login--------------

class Login(Resource):
    def get(self):
        format_user_login=reqparse.RequestParser()
        format_user_login.add_argument("username",type=str,help="Username is required",required=True)
        format_user_login.add_argument("password",type=str,help="Password is required",required=True)

        data=format_user_login.parse_args()

        check_record=User.query.filter_by(username=data['username'],password=data['password']).first()

        if check_record is None:
            abort(401,message="Not registered")
        token=jwt.encode({'USER_ID':check_record.id,'exp':datetime.utcnow() + timedelta(minutes=50)},app.config['SECRET_KEY'])
        return {"token":token.decode('utf-8')},200

api.add_resource(Login,'/login')





















#------User Registration------

class Register(Resource):
    def post(self):

        format_user_register=reqparse.RequestParser()
        format_user_register.add_argument("name",type=str,help="Name is required",required=True)
        format_user_register.add_argument("email",type=str,help="Email is required",required=True)
        format_user_register.add_argument("username",type=str,help="Username is required",required=True)
        format_user_register.add_argument("password",type=str,help="Password is required",required=True)
        
        data=format_user_register.parse_args()
        
        check_record_by_email = User.query.filter_by(email=data['email']).first()
        if check_record_by_email:
            abort(400,message="Email exists")
        
        check_record_by_username=User.query.filter_by(username=data['username']).first()
        if check_record_by_username:
            abort(400,message="Username exists")
        
        new_user=User(username=data['username'],password=data['password'],name=data['name'],email=data['email'])
        db.session.add(new_user) 
        db.session.commit()
        return {"message":"Registered successfully"},201

api.add_resource(Register,'/register')
































#----------Deck------------------
      
format_deck_output={
    "id":fields.Integer,
    "name":fields.String,
    "average_score":fields.Integer,
    "last_review_time":fields.String,
    "user_id":fields.Integer    
}

class DeckResource(Resource):
    @token_required
    @marshal_with(format_deck_output)
    def get(self):
        alldeck = Deck.query.filter_by(user_id=USER_ID).all()

        if len(alldeck)==0:
            return {"message":"No deck found"},403
        return alldeck

    @token_required    
    @marshal_with(format_deck_output)    
    def post(self):
        format_deck_input=reqparse.RequestParser()
        format_deck_input.add_argument("name",type=str,help="Deck name is required",required=True)
        
        data=format_deck_input.parse_args()

        check_deck=Deck.query.filter_by(user_id=USER_ID, name=data['name']).first()
        if check_deck is None:
            new_deck=Deck(name=data['name'],user_id=USER_ID)
            db.session.add(new_deck) 
            db.session.commit()
            return new_deck,201
        else:
            return {"message":"You already have this deck"},409

    @token_required        
    @marshal_with(format_deck_output)
    def put(self):
        format_deck_input=reqparse.RequestParser()
        format_deck_input.add_argument("id",type=int,help="Deck id is required",required=True)
        format_deck_input.add_argument("name",type=str,help="Deck name is required",required=True)
        data=format_deck_input.parse_args()

        check_deck=Deck.query.filter_by(user_id=USER_ID,id=data['id']).first()
        
        if check_deck is None:
            return {"message":"You don't have such a deck"},409

        check_deck.name=data['name']
        db.session.commit()
        return check_deck

    @token_required    
    def delete(self):
        format_deck_input=reqparse.RequestParser()
        format_deck_input.add_argument("id",type=int,help="Deck id is required",required=True)
        data=format_deck_input.parse_args()
        
        check_deck=Deck.query.filter_by(user_id=USER_ID,id=data['id']).first()
        
        if check_deck is None:
            return {"message":"You don't have such a deck"},409
        
        db.session.delete(check_deck)
        db.session.commit()
        return {'message':'Deck deleted'},204
   

api.add_resource(DeckResource,'/deck')


























#---------Card-------------------


format_card_output={
    "id":fields.Integer,
    "question":fields.String,
    "answer":fields.String,
    "last_review_time":fields.String,
    "score":fields.Integer,
    "deck_id":fields.Integer,
    "user_id":fields.Integer    
}


class CardResource(Resource):
    @token_required
    @marshal_with(format_card_output)
    def get(self):
        format_card_input=reqparse.RequestParser()
        format_card_input.add_argument("deck_id",type=int,help="Deck id is required",required=True)
        
        data=format_card_input.parse_args()

        allcard_of_deck=Card.query.filter_by(user_id=USER_ID,deck_id=data['deck_id']).all()
        
        if len(allcard_of_deck) ==0:
            return {"message":"Either deck id is wrong or No card"},403
        return allcard_of_deck

    @token_required
    @marshal_with(format_card_output)
    def post(self):
        format_card_input=reqparse.RequestParser()
        format_card_input.add_argument("question",type=str,help="Question is required",required=True)
        format_card_input.add_argument("answer",type=str,help="Answer is required",required=True)
        format_card_input.add_argument("deck_id",type=int,help="Deck id is required",required=True)
        
        data=format_card_input.parse_args()

        check_deck=Deck.query.filter_by(id=data['deck_id'],user_id=USER_ID).first()
        
        if check_deck is None:
            return {"message":"Sorry deck id not found"},404
        
        check_card=Card.query.filter_by(question=data['question'],deck_id=data['deck_id'],user_id=USER_ID).first()
        if check_card is not None:
            return {"message":"Card exists"},409

        new_card=Card(question=data['question'],answer=data['answer'],deck_id=data['deck_id'],user_id=USER_ID)
        db.session.add(new_card) 
        db.session.commit()
        return new_card,201

    @token_required        
    @marshal_with(format_card_output)
    def put(self):
        format_deck_input=reqparse.RequestParser()
        format_deck_input.add_argument("id",type=int,help="Card id is required",required=True)
        format_deck_input.add_argument("deck_id",type=int,help="Deck id is required",required=True)
        format_deck_input.add_argument("question",type=str,help="Question name is required",required=True)
        format_deck_input.add_argument("answer",type=str,help="Answer is required",required=True)
        format_deck_input.add_argument("last_review_time",type=str,help="Last review time",required=False)
        format_deck_input.add_argument("score",type=int,help="Score of this card",required=False)

        data=format_deck_input.parse_args()

        check_card=Card.query.filter_by(id=data['id'],deck_id=data['deck_id'],user_id=USER_ID).first()
        
        if check_card is None:
            return {"message":"You don't have such a Card"},409

        check_card.question=data['question']
        check_card.answer=data['answer']
        check_card.last_review_time=data['last_review_time']
        check_card.score=data['score']
        db.session.commit()
        return check_card    




    @token_required    
    def delete(self):
        format_card_input=reqparse.RequestParser()
        format_card_input.add_argument("id",type=int,help="Card id is required",required=True)
        format_card_input.add_argument("deck_id",type=int,help="Deck id is required",required=True)
        data=format_card_input.parse_args()
        
        check_card=Card.query.filter_by(id=data['id'],deck_id=data['deck_id'],user_id=USER_ID).first()
        
        if check_card is None:
            return {"message":"You don't have such a Card"},409
        
        db.session.delete(check_card)
        db.session.commit()
        return {'message':'Card deleted'},204


api.add_resource(CardResource,'/card')
        






















if __name__=='__main__':
    app.run(debug=True)