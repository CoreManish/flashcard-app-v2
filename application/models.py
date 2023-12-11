from application import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    webhook_url=db.Column(db.String(250))
    last_review_time = db.Column(db.Integer)
    # decks is not a column but is useful for finding all decks of a user
    # when you select a user say user1 then write user1.decks to see all decks of this user
    # user1=User.query.filter_by(username='manish').first()
    # user1.decks will give all decks
    # user1.decks[0] will give deck at 0th index
    # user1.decks[0].name will give name of deck at 0th index
    decks = db.relationship('Deck',cascade="all,delete", backref='decktouser')
    # backref=decktouser is useful when you select a deck and want to know info of user who created this deck
    # eg d=Deck.query.filter_by(id=3).first()
    # d.decktouser.id
    # d.decktouser.name
    cards = db.relationship('Card',cascade="all,delete", backref='cardtouser')


class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    average_score = db.Column(db.Integer)
    last_review_time = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cards = db.relationship('Card',cascade="all,delete", backref='cardtodeck')


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(150), nullable=False)
    answer = db.Column(db.String(200), nullable=False)
    last_review_time = db.Column(db.Integer)
    next_review_time = db.Column(db.Integer)
    score = db.Column(db.Integer)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
