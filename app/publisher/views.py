from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    jsonify,
    request
)
from flask_login import (
    current_user,
    login_required,
)

from app.auth.admin_decorators import publisher_login_required,check_confirmed
from app.publisher.forms import *

publisher = Blueprint('publisher', __name__)
photos = UploadSet('photos', IMAGES)

from app.publisher.countries import get_countries, get_arcode


@publisher.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        if current_user.role.index == 'publisher' and current_user.confirmed and not current_user.publisher\
            and request.path != url_for('publisher.edit_profile') and request.endpoint != 'static':
            flash('You need to finish editig your profile','cyan')
            return redirect(url_for('publisher.edit_profile'))



@publisher.route('/')
@login_required
@publisher_login_required
@check_confirmed
def dashboard():
    """Admin dashboard page."""
    listing_count = current_user.listings.count()
    booking_count = current_user.bookings_count()
    destination_count = current_user.listings.group_by(Listing.location).count()
    return render_template('publisher/index.html',listing_count=listing_count,booking_count=booking_count,destination_count=destination_count)


@publisher.route('/listings/<country>')
@login_required
@publisher_login_required
@check_confirmed
def listing(country):
    listings = Listing.query.filter_by(publisher=current_user, location=country).order_by(
        Listing.createdAt.desc()).all()
    return render_template('publisher/listing.html', items=listings, country=country)


@publisher.route('/listings/new', methods=('GET', 'POST'))
@login_required
@publisher_login_required
@check_confirmed
def newListing():
    form = ListingForm()
    form.price_type_id.choices = [(row.id, row.name) for row in
                                  Price.query.filter_by(publisher=current_user).order_by(Price.createdAt.desc()).all()]
    form.categories.choices = [(row.id, row.name) for row in Category.query.order_by(Category.createdAt.desc()).all()]
    form.location.choices = get_countries()
    if form.validate_on_submit():
        price = Price.query.filter_by(id=form.price_type_id.data).first_or_404()
        listing = Listing(location=form.location.data, duration=form.duration.data,
                          availability_from=form.availability_from.data,
                          availability_to=form.availability_to.data, long_description=form.long_description.data,
                          add_ons=form.add_ons.data, physical_condition=form.physical_condition.data,
                          price=price, policy=form.policy.data, package=form.package.data,
                          connectivity=form.connectivity.data, publisher=current_user)

        for row in form.categories.data:
            category = Category.query.filter_by(id=row).first_or_404()
            listing.categories.append(category)

        for item in form.activities.data:
            activities = Activity(activity=item['activity'], listing=listing)
            db.session.add(activities)

        for item in form.places.data:
            places = Place(place=item['place'].lower(), listing=listing)
            db.session.add(places)

        for item in form.days.data:
            days = Day(title=item['title'], day_by_day=item['day_by_day'], listing=listing)
            db.session.add(days)

        for image in form.images.data:
            if image['image'] is not None:
                img = photos.save(image['image'])
                image = Image(image_url=img, listing=listing)
                db.session.add(image)
        db.session.add(listing)
        db.session.commit()
        flash('Listing added successfully', 'green')
        return redirect(url_for('publisher.listing', country=listing.location))
    return render_template('publisher/add_listing.html', form=form)


@publisher.route('/listings/edit/<id>', methods=('GET', 'POST'))
@login_required
@publisher_login_required
@check_confirmed
def editListing(id):
    listing = Listing.query.filter_by(id=id, publisher=current_user).first_or_404()
    form = EditListingForm(obj=listing)
    form.location.choices = get_countries()
    if form.validate_on_submit():
        form.populate_obj(listing)
        db.session.commit()
        flash('Listing edited successfully', 'green')
        return redirect(url_for('publisher.listing', country=listing.location))
    return render_template('publisher/edit_listing.html', form=form)


@publisher.route('/listings/delete/<id>', methods=['POST'])
@login_required
@publisher_login_required
@check_confirmed
def deleteListing(id):
    listing = Listing.query.filter_by(id=id, publisher=current_user).first_or_404()
    db.session.delete(listing)
    db.session.commit()
    flash('Listing Deleted successfully', 'green')
    return redirect(url_for('publisher.listing', country=listing.location))


@publisher.route('/listings/publish/<id>')
@login_required
@publisher_login_required
@check_confirmed
def publishListing(id):
    listing = Listing.query.filter_by(id=id, publisher=current_user).first_or_404()
    if listing.published == True:
        listing.published = False
    else:
        listing.published = True
    db.session.commit()
    flash('Listing Published', 'green')
    return redirect(url_for('publisher.listing', country=listing.location))


@publisher.route('/category')
@login_required
@publisher_login_required
@check_confirmed
def category():
    categories = Category.query.order_by(Category.createdAt.desc()).all()
    return render_template('publisher/category.html', items=categories)


@publisher.route('/category/new', methods=('GET', 'POST'))
@login_required
@publisher_login_required
@check_confirmed
def newCategory():
    form = CategoryForm()
    if form.validate_on_submit():
        image = form.image.data
        if image:
            image = photos.save(form.image.data)
        category = Category(name=form.name.data, image_url=image)
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully', 'green')
        return redirect(url_for('publisher.category'))
    return render_template('publisher/add_category.html', form=form)


@publisher.route('/destinations')
@login_required
@publisher_login_required
@check_confirmed
def destination():
    destinations = Listing.query.filter_by(publisher=current_user).group_by(Listing.location)
    return render_template('publisher/destination.html', items=destinations)


@publisher.route('/packages')
@login_required
@publisher_login_required
@check_confirmed
def package():
    pricing = Price.query.filter_by(publisher=current_user).group_by(Price.location)
    arcodes = get_arcode()
    return render_template('publisher/package.html', items=pricing, arcodes=arcodes)


@publisher.route('/packages/<country>')
@login_required
@publisher_login_required
@check_confirmed
def pricing(country):
    pricing = Price.query.filter_by(publisher=current_user, location=country).order_by(Price.createdAt.desc()).all()
    return render_template('publisher/pricing.html', items=pricing, country=country)


@publisher.route('/pricing/new', methods=('GET', 'POST'))
@login_required
@publisher_login_required
@check_confirmed
def newPricing():
    form = PriceForm()
    form.location.choices = get_countries()
    if form.validate_on_submit():
        price = Price(name=form.name.data, location=form.location.data, total_price_adults=form.total_price_adults.data,
                      total_price_children=form.total_price_children.data,
                      price_per_day_adults=form.price_per_day_adults.data,
                      price_per_day_children=form.price_per_day_children.data, publisher=current_user)
        for item in form.includes.data:
            includes = Include(include=item['include'], price=price)
            db.session.add(includes)
        db.session.add(price)
        db.session.commit()
        flash('Pricing added successfully', 'green')
        return redirect(url_for('publisher.pricing', country=price.location))
    return render_template('publisher/add_price.html', form=form)


@publisher.route('/pricing/edit/<id>', methods=('GET', 'POST'))
@login_required
@publisher_login_required
@check_confirmed
def editPricing(id):
    pricing = Price.query.filter_by(id=id).first_or_404()
    form = EditPriceForm(obj=pricing)
    form.location.choices = get_countries()
    if form.validate_on_submit():
        form.populate_obj(pricing)
        db.session.commit()
        flash('Pricing edited successfully', 'green')
        return redirect(url_for('publisher.pricing', country=pricing.location))
    return render_template('publisher/add_price.html', form=form)


@publisher.route('/bookings')
@login_required
@publisher_login_required
@check_confirmed
def bookings():
    current_user.last_booking_read_time = datetime.utcnow()
    current_user.add_notification('unread_booking_count', 0)
    db.session.commit()
    bookings = Booking.query.join(
        Listing, (Listing.id == Booking.listing_id)).filter(
            Listing.publisher_id == current_user.id).order_by(Booking.createdAt.desc()).all()
    return render_template('publisher/bookings.html', bookings=bookings)


@publisher.route('/confirm_booking/<id>/<state>')
@login_required
@publisher_login_required
@check_confirmed
def confirm_booking(id,state):
    booking = Booking.query.filter_by(id=id).first_or_404()
    if booking.listing.publisher != current_user:
        return redirect(url_for('home.index'))
    booking.state = state
    db.session.commit()
    flash('Status Updated', 'green')
    return redirect(url_for('publisher.bookings'))


@publisher.route('/send_message/<id>', methods=['GET', 'POST'])
@login_required
@check_confirmed
def send_message(id):
    user = User.query.filter_by(id=id).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        flash('Your message has been sent.', 'green')
        return redirect(url_for('publisher.messages'))
    return render_template('publisher/send_message.html', title='Send Message', form=form, user=user)


@publisher.route('/messages')
@login_required
@check_confirmed
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).group_by(Message.sender_id)
    return render_template('publisher/messages.html', messages=messages)


@publisher.route('/notifications')
@login_required
@check_confirmed
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])


@publisher.route('/notifications_view')
@login_required
@check_confirmed
def notifications_view():
    bookings = current_user.user_notifications()
    return render_template('publisher/_notification.html', notifications=bookings)

@publisher.route('/settings', methods=['GET', 'POST'])
@login_required
@check_confirmed
def settings():
    form = EditPasswordForm()
    if form.validate_on_submit():
        current_user.password = form.password.data
        db.session.commit()
        flash('Password changed successfully', 'green')
        return redirect(url_for('publisher.settings'))
    return render_template('publisher/settings.html', form=form, title='Edit Password')


@publisher.route('/profile')
@login_required
@publisher_login_required
@check_confirmed
def profile():
    form = BannerForm()
    if form.validate_on_submit():
        logo = form.logo.data
        if logo:
            logo = photos.save(form.logo.data)
            current_user.publisher.logo = logo
        banner = form.banner.data
        if banner:
            banner = photos.save(form.banner.data)
            current_user.publisher.banner = banner
        db.session.commit()
        flash('Category added successfully', 'green')
        return redirect(url_for('publisher.category'))
    return render_template('publisher/profile.html', form=form)


@publisher.route('/edit_profile', methods=('GET', 'POST'))
@login_required
@publisher_login_required
@check_confirmed
def edit_profile():
    form = ProfileForm()
    publisher = current_user.publisher
    if publisher is not None:
        form = EditProfileForm(obj=publisher)
    if form.validate_on_submit():
        if publisher is not None:
            form.populate_obj(publisher)
        else:
            profile = Publisher(company_name=form.company_name.data, overview=form.overview.data,
                                facebook=form.facebook.data, twitter=form.twitter.data, instagram=form.instagram.data,
                                paypal=form.paypal.data, user=current_user)

            for item in form.phones.data:
                phones = Pubphones(phone_number=item['phone_number'], profile=profile)
                db.session.add(phones)

            for item in form.emails.data:
                emails = Pubemails(email=item['email'], profile=profile)
                db.session.add(emails)

            for item in form.locations.data:
                locations = Publocations(city=item['city'], country=item['country'], profile=profile)
                db.session.add(locations)

            db.session.add(profile)
        db.session.commit()
        flash('Profile Edited successfully', 'green')
        return redirect(url_for('publisher.profile'))
    return render_template('publisher/edit_profile.html', form=form)


@publisher.route('/edit_cover', methods=('GET', 'POST'))
@login_required
@publisher_login_required
@check_confirmed
def edit_cover():
    form = BannerForm()
    if form.validate_on_submit():
        logo = form.logo.data
        if logo:
            logo = photos.save(form.logo.data)
            current_user.publisher.logo = logo
        banner = form.banner.data
        if banner:
            banner = photos.save(form.banner.data)
            current_user.publisher.banner = banner
        db.session.commit()
        flash('Cover added successfully', 'green')
        return redirect(url_for('publisher.profile'))
    return render_template('publisher/edit_cover.html', form=form)


@publisher.route('/_get_pricing/')
def _get_pricing():
    location = request.args.get('location', '01', type=str)
    pricing = [(row.id, row.name) for row in
               Price.query.filter_by(location=location).order_by(Price.createdAt.desc()).all()]
    return jsonify(pricing)
