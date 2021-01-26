#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys

from flask_migrate import Migrate
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ARRAY, ForeignKey
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import app, db, Venue, Artist, Show



#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#


moment = Moment(app)
app.config.from_object('config')


# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


db.create_all()
db.session.commit()
def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

  # add real data : 
  # get all records of venues 
  venues = Venue.query.all ()
  data = [] 
  # to sort the states and cities 
  locationOfVenue = set () 
  upcomingShows = 0
  for venue in venues: 
    locationOfVenue.add ((venue.city , venue.state))
    # append the sorted set in data 
  for location in locationOfVenue:
    data.append ({
       'city': location[0] ,
      'state': location [1],
      'venues': []
    })
    
     # count the coming show in venues 
    for venue in venues:
      comingShows = venue.shows
      for show in comingShows:
        if show.start_time > datetime.now():
         upcomingShows+=1
        # after counting the shows now we must to add every venue to its correct states and city 
      for venueLocation in data:
        if venue.city == venueLocation [ 'city'] and venue.state == venueLocation ['state']:
          venueLocation['venues'].append ({
            'id':venue.id,
            'name': venue.name,
            'num_upcoming_shows': upcomingShows
          })


  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

 
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # get search word : 
  search_term = request.form.get('search_term', '')
  # get all query that same or contains letter same of search word 
  venues = Venue.query.filter (Venue.name.ilike(f'%{search_term}%')).all()
  data = []
  upcomingShowsCount = 0
  # count upComingShows. 
  for venue in venues:
    upcomingShow = venue.shows
    for show in upcomingShow:
      if show.start_time > datetime.now():
        upcomingShowsCount+=1
    data.append ({
      'id': venue.id , 
      'name': venue.name ,
      'num_upcoming_shows': upcomingShowsCount
    })

    response={
    "count": len(venues),
    "data": data
    }

  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

   venue = Venue.query.get (venue_id)
   past_shows_count = 0
   past_shows = [] 
   upcoming_shows_count = 0 
   upcoming_shows = [] 
   data =[]
   shows_query = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id)

   for show in shows_query: 
     if show.start_time > datetime.now():
      upcoming_shows_count +=1 
      upcoming_shows.append ({
        'venue_id': show.venue.id ,
        'venue_name': show.venue.name , 
        'venue_image_link': show.venue.image_link,
        'start_time': show.start_time 
      })
      if show.start_time < datetime.now():
       past_shows_count +=1
       past_shows.append ({
        'venue_id': show.venue.id ,
        'venue_name': show.venue.name , 
        'venue_image_link': show.venue.image_link,
        'start_time': show.start_time 
       })
      

     data= {
    "id": venue_id,
    "name": venue.name,
    "genres": venue.genres,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": past_shows_count,
    "upcoming_shows_count": upcoming_shows_count,
      }
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
 
 
   return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # create form : 
  form = VenueForm(request.form) 
  #insert object 
  venue = Venue (name=form.name.data , city=form.city.data ,
  state=form.state.data , address=form.address.data , phone=form.phone.data , 
  image_link = form.image_link.data , genres=form.genres.data , facebook_link=form.facebook_link.data ,
  seeking_talent = form.seeking_talent.data , seeking_description = form.seeking_description.data,
  website = form.website.data)
    # try to add object in data base 
  try:
      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
      flash('Venue ' + request.form['name'] + ' could not listed!')
  finally:
      db.session.close()


    
    


  
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  #flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  deletedVenue = Venue.query.get (venue_id)
  name = deletedVenue.name 
     # try to delete object fron the database 
  try:
      db.session.delete(deletedVenue)
      db.commit()
      flash('Venue ' + name+ ' was successfully deleted!')
  except:
      flash('Venue ' + name+ ' could not deleted!')
      db.session.rollback()
  finally:
      db.session.close()

  

  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # add real artists ..
  artists = Artist.query.all()
  data = [] 
  for artist in artists:
   data.append ({
     'id':artist.id,
     'name':artist.name })

   
   
  # TODO: replace with real data returned from querying the database

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():

   # get search word : 
  search_term = request.form.get('search_term', '')
  # get all query that same or contains letter same of search word 
  artists = Artist.query.filter (Artist.name.ilike(f'%{search_term}%')).all()
  data = []
  upcomingShowsCount = 0
  # count upComingShows. 
  for artist in artists:
    upcomingShow = artist.shows
    for show in upcomingShow:
      if show.start_time > datetime.now():
        upcomingShowsCount+=1
    data.append ({
      'id': artist.id , 
      'name': artist.name ,
      'num_upcoming_shows': upcomingShowsCount
    })

  response={
    "count": len(venues),
    "data": data
   }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

 

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
   artist = Artist.query.get (artist_id)
   past_shows_count = 0
   past_shows = [] 
   upcoming_shows_count = 0 
   upcoming_shows = [] 
   data = []
   shows_query = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id)

   for show in shows_query: 
  
     if show.start_time > datetime.now ():
      upcoming_shows_count+=1 
      upcoming_shows.append ({
        'venue_id': show.venue.id ,
        'venue_name': show.venue.name , 
        'venue_image_link': show.venue.image_link,
        'start_time': show.start_time 
      })
      if show.start_time < datetime.now ():
       past_shows_count+=1
       past_shows.append ({
        'venue_id': show.venue.id ,
        'venue_name': show.venue.name , 
        'venue_image_link': show.venue.image_link,
        'start_time': show.start_time 
       })
      

     
   data={
    "id": artist_id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": past_shows_count,
    "upcoming_shows_count": upcoming_shows_count,
       }


   return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  #get the record of artist 
  selectedArtist = Artist.query.get(artist_id)
  artist={
    "id": selectedArtist.id,
    "name": selectedArtist.name,
    "genres": selectedArtist.genres,
    "city": selectedArtist.city,
    "state": selectedArtist.state,
    "phone": selectedArtist.phone,
    "website": selectedArtist.website,
    "facebook_link": selectedArtist.facebook_link,
    "seeking_venue": selectedArtist.seeking_venue,
    "seeking_description": selectedArtist.seeking_description,
    "image_link": selectedArtist.image_link
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  error = False
  form = ArtistForm(request.form)
  neme = ''
  try: 
    artist = Artist.query.get (artist_id)
    artist.name = form.name.data 
    name =  artist.name
    artist.city = form.city.data 
    artist.state = form.state.data
    artist.phone=form.phone.data
    artist.genres =form.genres.data
    artist.seeking_venue = form.seeking_venue.data
    artist.seeking_description = form.Seeking_description.data
    artist.image_link = form.image_link.data
    artist.website = form.website.data
    artist.facebook_link = form.facebook_link.data
    db.session.commit()
    flash('Artist ' + name+ ' was successfully updated!')
  except:
    error = True
    db.session.rollback()
    flash('Artist ' + name+ ' could not updated!')
  finally:
    db.session.close()
  if error:
        abort(500)
  else:
     return redirect(url_for('index'))



  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  selectedVenue= Venue.query.get(venue_id)
  venue={
    "id": selectedVenue.id,
    "name": selectedVenue.name,
    "genres": selectedVenue.genres,
    'address': selectedVenue.address,
    "city": selectedVenue.city,
    "state": selectedVenue.state,
    "phone": selectedVenue.phone,
    "website": selectedVenue.website,
    "facebook_link": selectedVenue.facebook_link,
    "seeking_talent": selectedVenue.seeking_talent,
    "seeking_description": selectedVenue.seeking_description,
    "image_link": selectedVenue.image_link
  }

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  error = False
  form = VenueForm(request.form)
  neme = ''
  try: 
    venue = Venue.query.get (venue_id)
    venue.name = form.name.data 
    name =  venue.name
    venue.address = form.address.data
    venue.city = form.city.data 
    venue.state = form.state.data
    venue.phone=form.phone.data
    venue.genres =form.genres.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.Seeking_description.data
    venue.image_link = form.image_link.data
    venue.website = form.website.data
    venue.facebook_link = form.facebook_link.data
    db.session.commit()
    flash('Venue ' + name+ ' was successfully updated!')
  except:
    error = True
    db.session.rollback()
    flash('Venue ' + name+ ' could not updated!')
  finally:
    db.session.close()
  if error:
        abort(500)
  else:
        return redirect(url_for('index'))
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():


   # create form : 
  form = ArtistForm(request.form) 
  #insert object 
  artist = Artist (name=form.name.data , city=form.city.data ,
  state=form.state.data , phone=form.phone.data , 
  image_link = form.image_link.data , genres=form.genres.data , facebook_link=form.facebook_link.data ,
  seeking_venue = form.seeking_venue.data , seeking_description = form.seeking_description.data,
  website = form.website.data)
    # try to add object in data base 
  try:
      db.session.add(artist)
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
      flash('Artist ' + request.form['name'] + ' could not listed!')
  finally:
      db.session.close()

  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  #flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  #add real data .. 
  shows = Show.query.all ()
  data = []
  for show in shows:
    data.append ({
      'venue_id' : show.venue.id,
      'venue_name' : show.venue.name ,
      'artist_id' : show.artist.id,
      'artist_name' : show.artist.name, 
      'artist_image_link' : show.artist.image_link,
      'start_time' : show.start_time.isoformat() })
      


    

  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
 

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm(request.form)
  show = Show (venue_id = form.venue_id.data , artist_id = form.artist_id.data , 
  start_time = form.start_time.data)
  try:
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    flash('An error occurred. Show '+' could not be listed.')
  finally:
    db.session.close()
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
