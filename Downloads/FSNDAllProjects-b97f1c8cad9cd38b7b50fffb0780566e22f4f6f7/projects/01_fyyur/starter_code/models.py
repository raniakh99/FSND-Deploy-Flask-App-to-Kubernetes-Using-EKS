from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ARRAY, ForeignKey

app = Flask(__name__)
db = SQLAlchemy(app)
# Migrate ..
migrate = Migrate(app, db)

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    #add Missing Attributtes ( Genres , Website ,Seeking_talent , Seeking_description )
    genres=db.Column(ARRAY(db.String()))
    website=db.Column(db.String(120))
    seeking_talent=db.Column(db.Boolean ,default = False)
    seeking_description = db.Column ( db.String (120))

#add The Relationship with Show ( Parent is Venue and The Child is Show):

    shows = db.relationship('Show' , backref = 'venue' , lazy = True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
   
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    #add Missing Attributtes ( Genres , Website ,Seeking_talent , Seeking_description )
    genres=db.Column(ARRAY(db.String()))
    website=db.Column(db.String(120))
    seeking_venue=db.Column(db.Boolean , default = False )
    seeking_description = db.Column ( db.String (120))

#add The Relationship with Show ( Parent is Artist and The Child is Show):

    shows = db.relationship('Show' , backref = 'artist' , lazy = True)


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

# add Missing Model (Show)

class Show (db.Model):
  __tablename__ = 'Show'
  id = db.Column(db.Integer , primary_key =True)
  artist_id = db.Column (db.Integer , db.ForeignKey ( 'Artist.id') , nullable = False )
  venue_id = db.Column (db.Integer , db.ForeignKey('Venue.id') , nullable = False)
  start_time = db.Column(db.DateTime , nullable = False)

