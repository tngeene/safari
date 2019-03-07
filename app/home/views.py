from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,

)
from flask_login import (
    current_user,
    login_required,

)
from datetime import datetime
from app.models import *
from app.home.forms import Search, PaymentForm, BookingForm
from app.publisher.countries import get_arcode,get_country_code
from sqlalchemy import or_, and_, func

home = Blueprint('home', __name__)


@home.route('/', methods=['post', 'get'])
def index():
    form = Search()
    popular_packages = Listing.query.filter(Listing.status == True).limit(10)
    if Booking.query.count() > 3:
        popular_list = [row[0] for row in
                        db.session.query(Listing.id, func.count(Booking.listing_id).label('total')).join(
                            Booking).group_by(Listing).order_by('total DESC').all()]
        popular_packages = Listing.query.filter(Listing.id.in_(popular_list)).filter(Listing.status == True).limit(6)
    popular_operators = Publisher.query.join(
                                        User, (User.id == Publisher.user_id)).filter(User.status == True).order_by(Publisher.overal_ratings.desc()).limit(3)
    """Admin dashboard page."""
    return render_template('home/index.html', form=form,
                           popular_packages=popular_packages, popular_operators=popular_operators)


@home.route('/about')
def about():
    return render_template('home/about.html')


@home.route('/packages')
def listings():
    page = request.args.get('page', 1, type=int)
    categories = Category.query.all()
    listings = Listing.query.filter(Listing.status == True).order_by(Listing.rating.desc()).paginate(page,
                                                                                                     current_app.config[
                                                                                                         'POSTS_PER_PAGE'],
                                                                                                     False)
    if request.args.get('place') or request.args.get('date'):
        name = request.args.get('place') or ''
        date = request.args.get('date') or datetime.now()
        if isinstance(date, str):
            checkdate = datetime.strptime(date, '%m/%d/%Y')
            date = datetime.combine(checkdate, datetime.min.time())
        listings = get_search(name, date, page)
    next_url = url_for('home.listings', page=listings.next_num) if listings.has_next else None
    prev_url = url_for('home.listings', page=listings.prev_num) if listings.has_prev else None
    maxlist = Listing.query.filter(Listing.status == True).all()
    maxval = int(max(node.price.total_price_adults for node in maxlist)) if maxlist else 0
    arcodes = get_arcode()
    return render_template('home/list.html', listings=listings.items, next_url=next_url, prev_url=prev_url,
                           arcodes=arcodes, categories=categories, maxval=maxval)


@home.route('/packages/<package>')
def listings_by_package(package):
    packages = Listing.query.all()
    return render_template('home/packages.html', packages=packages)


@home.route('/packages/details/<id>')
def listings_by_details(id):
    listings = Listing.query.filter_by(id=id).first_or_404()
    form = BookingForm()
    form.total.data = listings.price.total_price_children + listings.price.total_price_adults
    if form.validate_on_submit():
        pass
    return render_template('home/details.html', listings=listings, form=form)


'''
implement payment using paypal
'''


@home.route('/booking/<id>', methods=['post', 'get'])
@login_required
def booking(id):
    booking = Booking.query.filter_by(id=id).first_or_404()
    form = PaymentForm()

    if form.validate_on_submit():

        year = form.years.data;
        month = form.month.data;
        billing_code = form.billing_zip_code.data;
        card_type = form.select_card.data;
        email = form.email.data;  # card identification number
        card_number = form.card_number.data;
        card_holder_name = form.card_holder_name.data;
        try:
            order = Order.query.filter_by(booking=booking).first_or_404();
            order_amount = order.grand_total;

            payment = Payment(booking=booking, user_id=current_user.id, years=year, month=month,
                              billing_zip_code=billing_code,
                              select_card=card_type,
                              card_identification_number=email, card_number=card_number,
                              card_holder_name=card_holder_name, amount=order_amount)
            db.session.add(payment)
        except Exception as e:
            print(e)

        """
            write code for payment i.e real payment transation
        """

        booking.state = 'paid'
        booking.status = True
        db.session.commit()

        return redirect(url_for('customer.dashboard'))
    return render_template('home/booking.html', form=form, booking=booking)


@home.route('/tour-operators')
def tour_operators_list():
    page = request.args.get('page', 1, type=int)
    publishers = Publisher.query.join(
        User, (User.id == Publisher.user_id)).filter(User.status == True).order_by(Publisher.overal_ratings.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('home.tour_operators', page=publishers.next_num) if publishers.has_next else None
    prev_url = url_for('home.tour_operators', page=publishers.prev_num) if publishers.has_prev else None
    offices = Publocations.query.group_by(Publocations.country)
    arcodes = get_arcode()
    return render_template('home/tour_operators.html', publishers=publishers.items, arcodes=arcodes, offices=offices,
                           next_url=next_url, prev_url=prev_url)


@home.route('/tour-operators/<publisher_id>/overview')
def tour_operator_details(publisher_id):
    publisher = User.query.filter_by(id=publisher_id).first()
    publisher_listings = Listing.query.filter_by(publisher_id=publisher_id)
    arcodes = get_arcode()
    return render_template('home/operator_details.html', publisher=publisher,
                           publisher_listings=publisher_listings, arcodes=arcodes)


@home.route('/tour-operators/<publisher_id>/packages')
def tour_operator_listings(publisher_id):
    page = request.args.get('page', 1, type=int)
    publisher = User.query.filter_by(id=publisher_id).first()
    publisher_listings = Listing.query.filter_by(publisher_id=publisher_id).filter(Listing.status == True).order_by(
        Listing.createdAt.desc()).paginate(page, 8, False)
    next_url = url_for('home.tour_operator_listings', publisher_id=publisher_id,
                       page=publisher_listings.next_num) if publisher_listings.has_next else None
    prev_url = url_for('home.tour_operator_listings', publisher_id=publisher_id,
                       page=publisher_listings.prev_num) if publisher_listings.has_prev else None
    arcodes = get_arcode()
    return render_template('home/operator_listings.html', publisher=publisher,
                           publisher_listings=publisher_listings.items, next_url=next_url, prev_url=prev_url,
                           arcodes=arcodes)


@home.route('/tour-operators/<publisher_id>/reviews')
def tour_operator_reviews(publisher_id):
    publisher = User.query.filter_by(id=publisher_id).first()
    publisher_listings = Listing.query.filter_by(publisher_id=publisher_id).filter(Listing.status == True)
    arcodes = get_arcode()
    return render_template('home/operator_reviews.html', publisher=publisher,
                           publisher_listings=publisher_listings, arcodes=arcodes)


@home.route('/tour-operators/<publisher_id>/destinations')
def tour_operator_destinations(publisher_id):
    publisher = User.query.filter_by(id=publisher_id).first()
    publisher_listings = Listing.query.filter_by(publisher_id=publisher_id).group_by(Listing.location)
    arcodes = get_arcode()
    return render_template('home/operator_destinations.html', publisher=publisher,
                           publisher_listings=publisher_listings, arcodes=arcodes)


@home.route('/tour-operators/<publisher_id>/contact')
def tour_operator_contact(publisher_id):
    publisher = User.query.filter_by(id=publisher_id).first()
    publisher_listings = Listing.query.filter_by(publisher_id=publisher_id)
    arcodes = get_arcode()
    return render_template('home/operator_contact.html', publisher=publisher,
                           publisher_listings=publisher_listings, arcodes=arcodes)


@home.route('/countries-and-parks')
def countries_and_parks_list():
    countries = Country.query.all()
    arcodes = get_arcode()
    return render_template('home/countries_and_parks.html', countries=countries,arcodes=arcodes)


@home.route('/countries/<country_id>/overview')
def country_details(country_id):
    country = Country.query.filter_by(id=country_id).first_or_404()
    return render_template('home/country_details.html', country=country)


@home.route('/park_details/<park_id>')
def park_details(park_id):
    park = Park.query.filter_by(id=park_id).first_or_404()
    return render_template('home/park_details.html', park=park)


@home.route('/countries/<country_id>/parks_and_reserves')
def country_parks_and_reserves(country_id):
    country = Country.query.filter_by(id=country_id).first_or_404()
    return render_template('home/country_parks_and_reserves.html', country=country)


@home.route('/countries/<country_id>/wildlife')
def country_wildlife(country_id):
    country = Country.query.filter_by(id=country_id).first_or_404()
    return render_template('home/country_wildlife.html', country=country)


@home.route('/countries/<country_id>/birds')
def country_birds(country_id):
    country = Country.query.filter_by(id=country_id).first_or_404()
    return render_template('home/country_birds.html', country=country)


@home.route('/contact-us')
def contact_us():
    return render_template('home/contact_us.html')


@home.route('/_get_category')
def _get_category():
    data = request.args
    page = request.args.get('page', 1, type=int)
    listings = get_categories(data, page)
    next_url = url_for('home.listings', page=listings.next_num) if listings.has_next else None
    prev_url = url_for('home.listings', page=listings.prev_num) if listings.has_prev else None
    arcodes = get_arcode()
    return render_template('home/_listings.html', listings=listings.items, arcodes=arcodes, next_url=next_url,
                           prev_url=prev_url)


@home.route('/_get_search')
def _get_search():
    data = request.args
    page = request.args.get('page', 1, type=int)
    listings = get_categories(data, page)
    next_url = url_for('home.listings', page=listings.next_num) if listings.has_next else None
    prev_url = url_for('home.listings', page=listings.prev_num) if listings.has_prev else None
    arcodes = get_arcode()
    return render_template('home/_listings.html', listings=listings.items, arcodes=arcodes, next_url=next_url,
                           prev_url=prev_url)


@home.route('/_get_range')
def _get_range():
    max_val = request.args.get('maxval', 1, type=int)
    min_val = request.args.get('minval', 1, type=int)
    page = request.args.get('page', 1, type=int)
    listings = get_range(max_val, min_val, page)
    next_url = url_for('home.listings', page=listings.next_num) if listings.has_next else None
    prev_url = url_for('home.listings', page=listings.prev_num) if listings.has_prev else None
    arcodes = get_arcode()
    return render_template('home/_listings.html', listings=listings.items, arcodes=arcodes, next_url=next_url,
                           prev_url=prev_url)


@home.route('/_get_ratings')
def _get_ratings():
    data = request.args
    page = request.args.get('page', 1, type=int)
    listings = get_ratings(data, page)
    next_url = url_for('home.listings', page=listings.next_num) if listings.has_next else None
    prev_url = url_for('home.listings', page=listings.prev_num) if listings.has_prev else None
    arcodes = get_arcode()
    return render_template('home/_listings.html', listings=listings.items, arcodes=arcodes, next_url=next_url,
                           prev_url=prev_url)


@home.route('/_get_office')
def _get_office():
    data = request.args
    page = request.args.get('page', 1, type=int)
    publishers = User.get_operators(data, page)
    next_url = url_for('home.tour_operators', page=publishers.next_num) if publishers.has_next else None
    prev_url = url_for('home.tour_operators', page=publishers.prev_num) if publishers.has_prev else None
    arcodes = get_arcode()
    return render_template('home/_tour_operators.html', publishers=publishers.items, arcodes=arcodes, next_url=next_url,
                           prev_url=prev_url)


@home.route('/_get_tour_ratings')
def _get_tour_ratings():
    data = request.args
    page = request.args.get('page', 1, type=int)
    publishers = User.get_tour_ratings(data, page)
    next_url = url_for('home.tour_operators', page=publishers.next_num) if publishers.has_next else None
    prev_url = url_for('home.tour_operators', page=publishers.prev_num) if publishers.has_prev else None
    arcodes = get_arcode()
    return render_template('home/_tour_operators.html', publishers=publishers.items, arcodes=arcodes, next_url=next_url,
                           prev_url=prev_url)


@home.route('/privacy_policy')
def privacy():
    return render_template('home/privacy_policy.html')
