from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)
from flask_login import (
    current_user,
    login_required,
)

from flask_rq import get_queue
from app.models.listings import *
from app.models.bookings import *
from app.models.offers import *
from app.models.users import *
from app.models.orders import *
from app.home.forms import *
from app.customer.forms import *
from app.auth.forms import *
from app import db
from app.email import send_email
from app.models import User
from app.auth.email import send_password_reset_email
from app.auth.admin_decorators import check_confirmed

customer = Blueprint('customer', __name__)


@customer.route('/')
@login_required
@check_confirmed
def dashboard():
    """Admin dashboard page."""

    cancelled = current_user.bookings.filter_by(state='cancelled').count()
    accepted = current_user.bookings.filter_by(state='accepted').count()

    return render_template('customer/index.html', cancelled=cancelled, accepted=accepted)


@customer.route('/book/<id>', methods=['post', 'get'])
@login_required
@check_confirmed
def book(id):
    """Admin dashboard page."""
    list_booked = Listing.query.filter_by(id=id).first_or_404()
    form = BookingForm()
    if form.validate_on_submit():
        if current_user == list_booked.publisher:
            return redirect(url_for('home.index'))
        booked_list = Booking(listing=list_booked, user=current_user)
        # create order during booking

        adults = form.adults.data
        kids = form.kids.data
        grand_total = form.total.data
        order = Order(booking=booked_list, departure_date=form.departure_date.data, children=kids,
                      adults=adults, grand_total=grand_total)  # add more order details
        db.session.add(booked_list)
        db.session.add(order)
        list_booked.publisher.add_notification('unread_booking_count', list_booked.publisher.new_bookings())
        db.session.commit()
        flash('Booked successfully', 'green')
        return redirect(url_for('customer.dashboard'))
    return render_template('home/details.html', form=form, listings=list_booked)


@customer.route('/booking/communicate')
@login_required
@check_confirmed
def communicateaboutbook():
    """Admin dashboard page."""
    return redirect(url_for('customer.dashboard'))


@customer.route('/view/booking/<status>')
@login_required
@check_confirmed
def view_bookings_by(status):
    """Admin dashboard page."""
    bookings = Booking.query.filter_by(user=current_user, state=status).all()
    return render_template('customer/booking_by_status.html', bookings=bookings, status=status)


@customer.route('/view/booking')
@login_required
@check_confirmed
def view_bookings():
    """Admin dashboard page."""
    bookings = Booking.query.filter_by(user=current_user).all()
    return render_template('customer/bookings.html', bookings=bookings)


@customer.route('/view/payments')
@login_required
@check_confirmed
def view_payments():
    """Admin dashboard page."""
    payments = Payment.query.filter_by(user=current_user).all()

    return render_template('customer/payments.html', payments=payments)


@customer.route('/accept_offer')
@login_required
@check_confirmed
def accept_offer():
    """Admin dashboard page."""
    return redirect(url_for('customer.dashboard'))


@customer.route('/communicate_to_publisher')
def communicate_to_publisher():
    """Admin dashboard page."""
    return render_template('customer/app-email.html')


@customer.route('/decline_offer')
def decline_offer():
    """Admin dashboard page."""
    return render_template('customer/index.html')


@customer.route('/review/<what>/<id>', methods=['post', 'get'])
@login_required
@check_confirmed
def review(what, id):
    """Admin dashboard page."""

    form = ReviewForm()
    form.stars.choices = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    if form.validate_on_submit():

        if what == 'listing':
            listing = Listing.query.filter_by(id=id).first_or_404()
            stars = form.stars.data
            comment = form.comment.data
            review = Review(user=current_user, listing=listing, value=stars, comment=comment)
            db.session.add(review)
            total_score=listing.overal_ratings + 1
            weighted_score=((listing.rating * listing.overal_ratings) + stars) / (total_score)
            listing.rating=weighted_score
            listing.overal_ratings=total_score
            db.session.commit()
            return redirect(url_for('customer.dashboard'))
        elif what == 'publisher':
            user = User.query.filter_by(id=id).first_or_404()
            stars = form.stars.data
            comment = form.comment.data
            review = Review(user=current_user, publisher=user, value=stars, comment=comment)
            db.session.add(review)
            total_score=user.publisher.overal_ratings + 1
            weighted_score=((user.publisher.rating * user.publisher.overal_ratings) + stars) / (total_score)
            user.publisher.rating=weighted_score
            user.publisher.overal_ratings=total_score
            db.session.commit()
            return redirect(url_for('customer.dashboard'))
    return render_template('customer/review.html', what=what, form=form, id=id)


@customer.route('/profile', methods=['post', 'get'])
@login_required
@check_confirmed
def profile():
    """Admin dashboard page."""

    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.commit()
        return redirect(url_for('customer.dashboard'))

    return render_template('customer/user-profile-page.html', form=form)


@customer.route('/settings', methods=['post', 'get'])
@login_required
@check_confirmed
def settings():
    """Admin dashboard page."""

    if current_user.is_anonymous:
        return redirect(url_for('home.index'))
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.', 'green')
            return redirect(url_for('customer.dashboard'))
        else:
            flash('Original password is invalid.', 'orange')
    return render_template('account/reset_password.html', form=form)
