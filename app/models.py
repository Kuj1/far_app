from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class CardsSellBr(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_number = db.Column(db.Integer, unique=True, sqlite_on_conflict_unique='REPLACE')
    section = db.Column(db.String)
    title = db.Column(db.String)
    photo = db.Column(db.String)
    date_post = db.Column(db.Integer)
    author_card = db.Column(db.String)
    region_address = db.Column(db.String)
    street_address = db.Column(db.String)
    size = db.Column(db.Integer)
    price = db.Column(db.Integer)
    contacts = db.Column(db.String)


class CardsRentBr(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    card_number = db.Column(db.Integer, unique=True, sqlite_on_conflict_unique='REPLACE')
    section = db.Column(db.String)
    title = db.Column(db.String)
    photo = db.Column(db.String)
    date_post = db.Column(db.Integer)
    author_card = db.Column(db.String)
    region_address = db.Column(db.String)
    street_address = db.Column(db.String)
    size = db.Column(db.Integer)
    price = db.Column(db.Integer)
    price_for_what = db.Column(db.String)
    contacts = db.Column(db.String)


class CardsSellLand(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    card_number = db.Column(db.Integer, unique=True, sqlite_on_conflict_unique='REPLACE')
    section = db.Column(db.String)
    title = db.Column(db.String)
    photo = db.Column(db.String)
    date_post = db.Column(db.Integer)
    author_card = db.Column(db.String)
    placement = db.Column(db.String)
    size = db.Column(db.Integer)
    price = db.Column(db.Integer)
    price_for_what = db.Column(db.String)
    status = db.Column(db.String)
    restrictions = db.Column(db.String)
    cadastr_number_f = db.Column(db.Integer)
    cadastr_number_s = db.Column(db.Integer)
    electricity = db.Column(db.String)
    water = db.Column(db.String)
    roads = db.Column(db.String)
    contacts = db.Column(db.String)


class CardsRentLand(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    card_number = db.Column(db.Integer, unique=True, sqlite_on_conflict_unique='REPLACE')
    section = db.Column(db.String)
    title = db.Column(db.String)
    photo = db.Column(db.String)
    date_post = db.Column(db.Integer)
    author_card = db.Column(db.String)
    placement = db.Column(db.String)
    size = db.Column(db.Integer)
    price = db.Column(db.Integer)
    price_for_what = db.Column(db.String)
    status = db.Column(db.String)
    restrictions = db.Column(db.String)
    cadastr_number_f = db.Column(db.Integer)
    cadastr_number_s = db.Column(db.Integer)
    electricity = db.Column(db.String)
    water = db.Column(db.String)
    roads = db.Column(db.String)
    contacts = db.Column(db.String)


@login.user_loader
def load_user(ids):
    return User.query.get(int(ids))
