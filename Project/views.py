from flask import Blueprint, request, flash, redirect, url_for
from flask import render_template
from flask_login import login_required, current_user
from . import models
from . import db
from datetime import datetime

views = Blueprint('views',__name__)

@views.route('/', methods = ['get','post'])
@login_required
def home():
    if current_user.isadmin == True :
        return render_template("admin_dashboard.html", user = current_user)
    else:

        if request.method == "POST":
            show_name = request.form.get('show_name')
            tags = request.form.get('tags')
            rating = request.form.get('rating')


            results = models.Show.query.filter((models.Show.show_name == show_name) | (models.Show.tags == tags) | (models.Show.rating == rating)).limit(5).all()
            
            users = db.session.query(models.User).all()
            return render_template("user_dashboard.html", user = current_user, users=users, results = results)

        users = db.session.query(models.User).all()
        return render_template("user_dashboard.html", user = current_user, users=users, results = [])


@views.route('/venue', methods = ['get','post'])
@login_required
def venue():
   
    if request.method == "POST":
        venue_name = request.form.get('venue_name')
        place = request.form.get('place')
        capacity = request.form.get('capacity')

        if (len(venue_name) < 1):
            flash("Venue Name is too short", category='error')
        elif(len(place)<1):
            flash("Place is not specified properly", category='error')
        elif(int(capacity) < 10):
            flash("Capacity must be more than 10",category='error')
        else:
            new_venue = models.Venue(venue_name = venue_name, place = place, capacity = capacity, owner = current_user.id)
            db.session.add(new_venue)
            db.session.commit()
            flash("Venue added!", category='success')
            return redirect(url_for('views.home'))
        
    return render_template("venue.html", user = current_user, editing = False)

@views.route('/show',methods = ['get','post'])
@login_required
def show():
    venue_id = request.args['id']
    if request.method == "POST":
        show_name = request.form.get('show_name')
        rating = request.form.get('rating')
        start_time = datetime.strptime(request.form.get('start_time'),'%H:%M').time()
        end_time = datetime.strptime(request.form.get('end_time'),'%H:%M').time()
        tags = request.form.get('tags')
        price = request.form.get('price')

        if (len(show_name) < 1):
            flash("Show Name is too short", category='error')
        elif(int(rating)<0 and int(rating)>5):
            flash("Invalid Rating", category='error')
        elif(int(price) < 0):
            flash("Price can\'t be less than 0",category='error')
        else:
            new_show = models.Show(show_name = show_name, rating = rating, start_time = start_time, end_time = end_time, tags = tags, price = price, hall = venue_id)
            db.session.add(new_show)
            db.session.commit()
            flash("Show added!", category='success')
            return redirect(url_for('views.home'))
        
    return render_template("shows.html", user = current_user, editing = False)


@views.route('/booking',methods = ['get','post'])
@login_required
def booking():
    show_id = request.args['show_id']
    venue_id = request.args['venue_id']
    current_venue = models.Venue.query.filter_by(id = int(venue_id)).first()
    current_show = models.Show.query.filter_by(id = int(show_id)).first()
    
    if request.method == "POST":
        tickets = request.form.get('tickets')

        if (int(tickets) < 1):
            flash("Minimum 1 ticket should be booked", category='error')
        elif(int(tickets) > current_venue.capacity):
            flash("Tickets exceeding the available seats",category='error')
        else:
            new_booking = models.Booking(tickets = int(tickets), show = int(show_id), user = current_user.id,)
            db.session.add(new_booking)
            db.session.commit()
            flash("Tickets Booked successfully!", category='success')
            return redirect(url_for('views.home'))

    return render_template("booking.html", user = current_user, venue = current_venue, show = current_show)

@views.route('/user_bookings',methods = ['get'])
@login_required
def user_bookings():
    booked_tickets = current_user.bookings

    shows = []
    for booking in booked_tickets:
        user_show = models.Show.query.filter_by(id = int(booking.show)).first()
        shows.append(user_show)
        
    for i in range(len(shows)):
        shows[i].tickets = booked_tickets[i].tickets

    return render_template("user_bookings.html",user = current_user, shows = shows)

@views.route('/edit_show',methods = ['get','post'])
@login_required
def edit_show():
    show_id = request.args['id']
    show = models.Show.query.get(int(show_id))


    if request.method == "POST":
        show_name = request.form.get('show_name')
        rating = request.form.get('rating')
        start_time = datetime.strptime(request.form.get('start_time'),'%H:%M').time()
        end_time = datetime.strptime(request.form.get('end_time'),'%H:%M').time()
        tags = request.form.get('tags')
        price = request.form.get('price')

        if (len(show_name) < 1):
            flash("Show Name is too short", category='error')
        elif(int(rating)<0 and int(rating)>5):
            flash("Invalid Rating", category='error')
        elif(int(price) < 0):
            flash("Price can\'t be less than 0",category='error')
        else:
            current_show = models.Show.query.filter_by(id = int(show_id)).first()
            current_show.show_name = show_name
            current_show.rating = rating
            current_show.start_time = start_time
            current_show.end_time = end_time
            current_show.tags = tags
            current_show.price = price
            db.session.commit()
            flash("Show updated!", category='success')
            return redirect(url_for('views.home'))
        
    return render_template("shows.html", user = current_user, editing = True, show = show)


@views.route('/delete_show',methods = ['get'])
@login_required
def delete_show():
    show_id = request.args['id']
    show = models.Show.query.get(int(show_id))
    db.session.delete(show)
    db.session.commit()
    flash("Show deleted!", category='success')
    return redirect(url_for('views.home'))

@views.route('/edit_venue',methods = ['get','post'])
@login_required
def edit_venue():
    venue_id = request.args['id']
    venue = models.Venue.query.get(int(venue_id))

    if request.method == "POST":
        venue_name = request.form.get('venue_name')
        place = request.form.get('place')
        capacity = request.form.get('capacity')

        if (len(venue_name) < 1):
            flash("Venue Name is too short", category='error')
        elif(len(place)<1):
            flash("Place is not specified properly", category='error')
        elif(int(capacity) < 10):
            flash("Capacity must be more than 10",category='error')
        else:
            current_venue = models.Venue.query.filter_by(id = int(venue_id)).first()
            current_venue.venue_name = venue_name
            current_venue.place = place
            current_venue.capacity = capacity
            db.session.commit()
            flash("Venue updated!", category='success')
            return redirect(url_for('views.home'))
        
    return render_template("venue.html", user = current_user, editing = True, venue = venue)

@views.route('/delete_venue',methods = ['get'])
@login_required
def delete_venue():
    venue_id = request.args['id']
    venue = models.Venue.query.get(int(venue_id))
    db.session.delete(venue)
    db.session.commit()
    flash("Venue deleted!", category='success')
    return redirect(url_for('views.home'))