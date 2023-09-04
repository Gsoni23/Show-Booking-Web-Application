from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(150),unique = True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    isadmin = db.Column(db.Boolean, default = False)
    venues = db.relationship('Venue')
    bookings = db.relationship('Booking')

    def __repr__(self) -> str:
        return f"<User name={self.name} email={self.email} isadmin={self.isadmin} venues={self.venues}>"


class Venue (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    venue_name = db.Column(db.String(250))
    place = db.Column(db.String(250))
    capacity = db.Column(db.Integer)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    shows = db.relationship('Show')

    def __repr__(self) -> str:
        return f"<id = {self.id} Venue name={self.venue_name} place={self.place} capacity={self.capacity} owner={self.owner} shows = {self.shows}"

class Show(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    show_name = db.Column(db.String(250))
    rating = db.Column(db.Integer)
    start_time = db.Column(db.Time(timezone = True), default = func.now())
    end_time = db.Column(db.Time(timezone = True), default = func.now())
    tags = db.Column(db.String(1000))
    price = db.Column(db.Integer)
    hall = db.Column(db.Integer, db.ForeignKey('venue.id', ondelete = 'CASCADE'))
    book_ings = db.relationship('Booking')

    def __repr__(self) -> str:
        return f"<id = {self.id} price = {self.price}"
        
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    tickets = db.Column(db.Integer)
    show = db.Column(db.Integer, db.ForeignKey('show.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f"<id = {self.id} tickets = {self.tickets} show = {self.show}"



  