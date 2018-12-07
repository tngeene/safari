from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
)

from app.models import *
from app.decorators import admin_required
from flask_login import current_user, login_required
from app.admin.forms import *
from app.auth.forms import *
from flask_rq import get_queue
from app.email import send_email
from app.auth.email import send_confirm_email
from app.auth.email import send_password_reset_email
from app.auth.admin_decorators import check_confirmed

admin = Blueprint('admin', __name__)
photos = UploadSet('photos', IMAGES)


@admin.route('/')
@login_required
@admin_required
@check_confirmed
def dashboard():
    """Admin dashboard page."""
    bookings = Booking.query.all()
    listings = Listing.query.all()
    croles = Role.query.filter_by(index='customer').first_or_404()
    customers = croles.users
    proles = Role.query.filter_by(index='publisher').first_or_404()
    publishers = proles.users
    bookingsCount = Booking.query.count()
    listingsCount = Listing.query.count()
    publishersCount = publishers.count()
    customersCount = customers.count()
    titles= [listing.title for listing in listings]
    list=[]
    for listing in listings:
        count = Booking.query.filter_by(listing_id=listing.id).count()
        list.append(count)
    return render_template('admin/index.html', bookings=bookings, list=list, listings=listings, titles=titles,
                           bookingsCount=bookingsCount, listingsCount=listingsCount, publishersCount=publishersCount,
                           customersCount=customersCount, publishers=publishers, customers=customers)


@admin.route('/all_publishers')
@login_required
@admin_required
@check_confirmed
def publishers():
    """Publisher dashboard page."""
    roles=Role.query.filter_by(index='publisher').first_or_404()
    publishers = roles.users
    return render_template('admin/publishers.html', publishers=publishers)


@admin.route('/all_payments')
@login_required
@admin_required
@check_confirmed
def payments():
    """Payment dashboard page."""
    return render_template('admin/blank.html')


@admin.route('/all_customers')
@login_required
@admin_required
def customers():
    """Admin dashboard page."""
    roles = Role.query.filter_by(index='customer').first_or_404()
    customers = roles.users
    return render_template('admin/customers.html', customers=customers)


@admin.route('/all_bookings')
@login_required
@admin_required
@check_confirmed
def bookings():
    """Admin dashboard page."""
    bookings = Booking.query.all()
    return render_template('admin/bookings.html', bookings=bookings)


@admin.route('/all_listings')
@login_required
@admin_required
def listings():
    """All Listings Page."""
    listings = Listing.query.all()

    return render_template('admin/listings.html', listings=listings)


@admin.route('/listing_details')
@login_required
@admin_required
@check_confirmed
def listing_details():
    """All Listings Page."""
    id = request.args.get('since', 0, type=int)
    listing = Listing.query.filter_by(id=id).first_or_404()
    return render_template('admin/_listing_details.html', listing=listing)


@admin.route('/view_publisher/<user_id>')
@login_required
@admin_required
@check_confirmed
def publisher_by(user_id):
    """Publisher dashboard page."""
    roles = Role.query.filter_by(index='publisher').first_or_404()
    publishers = roles.users
    return render_template('admin/manage_user.html', publishers=publishers)


@admin.route('/view_customer/<id>')
@login_required
@admin_required
@check_confirmed
def customer_id(id):
    """Admin dashboard page."""
    return render_template('admin/index.html')


@admin.route('/view_booking/<id>')
@login_required
@admin_required
@check_confirmed
def booking_id(id):
    """Admin dashboard page."""
    return render_template('admin/index.html')


@admin.route('/view_listing/<id>')
@login_required
@admin_required
@check_confirmed
def listing_id(id):
    """Admin dashboard page."""
    return render_template('admin/index.html')


@admin.route('/add_new_user', methods=['GET', 'POST'])
@login_required
@admin_required
@check_confirmed
def new_user():
    """Create a new user."""
    form = NewUserForm()
    if form.validate_on_submit():
        user = User(
            role=form.role.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User {} successfully created'.format(user.full_name()),
              'form-success')
    return render_template('admin/new_user.html', form=form)


@admin.route('/invite-user', methods=['GET', 'POST'])
@login_required
@admin_required
@check_confirmed
def invite_user():
    """Invites a new user to create an account and set their own password."""
    form = InviteUserForm()
    if form.validate_on_submit():
        user = User(
            role=form.role.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        invite_link = url_for(
            'account.join_from_invite',
            user_id=user.id,
            token=token,
            _external=True)
        get_queue().enqueue(
            send_email,
            recipient=user.email,
            subject='You Are Invited To Join',
            template='account/email/invite',
            user=user,
            invite_link=invite_link
        )
        flash('User {} successfully invited'.format(user.full_name()),
              'form-success')
    return render_template('admin/invite_user.html', form=form)


@admin.route('/all_users')
@login_required
@admin_required
@check_confirmed
def registered_users():
    """View all registered users."""
    users = User.query.all()
    roles = Role.query.all()
    return render_template(
        'admin/registered_users.html', users=users, roles=roles)


@admin.route('/view_user/<int:user_id>')
@admin.route('/view_user/<int:user_id>/info')
@login_required
@admin_required
@check_confirmed
def user_info(user_id):
    """View a user's profile."""
    user = User.query.filter_by(id=user_id).first()
    bookings = Booking.query.filter_by(user_id=user_id).all()
    bookingsCount = Booking.query.filter_by(user_id=user_id).count()
    listingsCount = Listing.query.filter_by(publisher_id=user_id).count()
    if user is None:
        abort(404)
    return render_template('admin/manage_user.html', user=user, bookings=bookings, bookingsCount=bookingsCount,
                           listings=listings, listingsCount=listingsCount)


@admin.route('/user/<int:user_id>/change-email', methods=['GET', 'POST'])
@login_required
@admin_required
@check_confirmed
def change_user_email(user_id):
    """Change a user's email."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    form = ChangeUserEmailForm()
    if form.validate_on_submit():
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        flash('Email for user {} successfully changed to {}.'.format(
            user.full_name(), user.email), 'form-success')
    return render_template('admin/manage_user.html', user=user, form=form)


@admin.route(
    '/user/<int:user_id>/change-account-type', methods=['GET', 'POST'])
@login_required
@admin_required
@check_confirmed
def change_account_type(user_id):
    """Change a user's account type."""
    if current_user.id == user_id:
        flash('You cannot change the type of your own account. Please ask '
              'another administrator to do this.', 'error')
        return redirect(url_for('admin.user_info', user_id=user_id))

    user = User.query.get(user_id)
    if user is None:
        abort(404)
    form = ChangeAccountTypeForm()
    if form.validate_on_submit():
        user.role = form.role.data
        db.session.add(user)
        db.session.commit()
        flash('Role for user {} successfully changed to {}.'.format(
            user.full_name(), user.role.name), 'form-success')
    return render_template('admin/manage_user.html', user=user, form=form)


@admin.route('/user/<int:user_id>/delete')
@login_required
@admin_required
@check_confirmed
def delete_user_request(user_id):
    """Request deletion of a user's account."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('admin/manage_user.html', user=user)


@admin.route('/user/<int:user_id>/_delete')
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user's account."""
    if current_user.id == user_id:
        flash('You cannot delete your own account. Please ask another '
              'administrator to do this.', 'error')
    else:
        user = User.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        flash('Successfully deleted user %s.' % user.full_name(), 'green')
    return redirect(url_for('admin.registered_users'))


@admin.route('/approve_listing/<listing_id>')
@login_required
@admin_required
@check_confirmed
def approve_listing(listing_id):
    listing = Listing.query.filter_by(id=listing_id).first_or_404()
    if listing.status == 1:
        listing.status = 0
        flash('Listing Already Approved.')
    else:
        listing.status = 1
    db.session.commit()
    flash('Successfully Approved Listing', 'green')
    return redirect(url_for('admin.listings'))


@admin.route('/publisher/<int:user_id>/_suspend')
@login_required
@admin_required
@check_confirmed
def suspend(user_id):
    """Suspend a user's account."""
    user = User.query.filter_by(id=user_id).first()
    if current_user.id == user_id:
        flash('You cannot suspend your own account. Please ask another '
              'administrator to do this.', 'error')
    else:
        if user.status == 1:
            user.status = 0
        else:
            user.status = 1
        db.session.commit()
        flash('Successfully suspended user %s.' % user.full_name(), 'green')
    return redirect(url_for('admin.user_info', user_id=user.id))


@admin.route('/countries/view_all')
@login_required
@admin_required
@check_confirmed
def countries():
    allcountries = Country.query.all()

    return render_template('admin/all_countries.html', allcountries=allcountries)


@admin.route('/countries/add', methods=['GET', 'POST'])
@login_required
@admin_required
@check_confirmed
def add_country():
    allcountries = Country.query.all()
    """Create a new country."""
    form = AddCountryForm()
    if form.validate_on_submit():
        image = form.image.data
        if image:
            image = photos.save(form.image.data)
        newcountry = Country(
            name=form.name.data,
            description=form.description.data,
            overview=form.overview.data,
            climate=form.climate.data,
            image_url=image,
            best_time_to_visit=form.best_time_to_visit.data
        )
        db.session.add(newcountry)
        db.session.commit()
        flash('New Country created', 'green')
        return redirect(url_for('admin.countries'))
    return render_template('admin/new_country.html', allcountries=allcountries, form=form)


@admin.route('/countries/edit/<id>', methods=('GET', 'POST'))
@login_required
@admin_required
@check_confirmed
def edit_country(id):
    country = Country.query.filter_by(id=id).first_or_404()
    form = EditCountryForm(obj=country)
    if form.validate_on_submit():
        image = form.image_url.data
        if image:
            image = photos.save(form.image_url.data)
            form.image_url.data = image
        form.populate_obj(country)
        db.session.commit()
        flash('Country edited successfully', 'green')
        return redirect(url_for('admin.countries', country=country))
    return render_template('admin/edit_country.html', form=form, country=country)


@admin.route('/countries/delete/<id>', methods=['POST'])
@login_required
@admin_required
@check_confirmed
def delete_country(id):
    country = Country.query.filter_by(id=id).first_or_404()
    db.session.delete(country)
    db.session.commit()
    flash('Country Deleted successfully', 'green')
    return redirect(url_for('admin.countries'))


@admin.route('/birds/view_all')
@login_required
@admin_required
@check_confirmed
def birds():
    allbirds = Bird.query.all()

    return render_template('admin/all_birds.html', allbirds=allbirds)


@admin.route('/birds/add', methods=['GET', 'POST'])
@login_required
@admin_required
@check_confirmed
def add_bird():
    allbirds = Bird.query.all()
    """Create a new bird."""
    form = AddBirdForm()
    form.park.choices = [(row.id, row.name) for row in Park.query.all()]
    if form.validate_on_submit():
        image = form.image.data
        if image:
            image = photos.save(form.image.data)
        park = Park.query.filter_by(id=form.park.data).first_or_404()
        newbird = Bird(
            name=form.name.data,
            description=form.description.data,
            image_url=image,
            park=park
        )
        db.session.add(newbird)
        db.session.commit()
        flash('New Bird created', 'green')
        return redirect(url_for('admin.birds'))
    return render_template('admin/new_bird.html', allbirds=allbirds, form=form)


@admin.route('/birds/edit/<id>', methods=('GET', 'POST'))
@login_required
@admin_required
@check_confirmed
def edit_bird(id):
    bird = Bird.query.filter_by(id=id).first_or_404()
    form = EditBirdForm(obj=bird)
    park_id = bird.park.id
    park_name = bird.park.name
    if form.validate_on_submit():
        image = form.image_url.data
        if image:
            image = photos.save(form.image_url.data)
            form.image_url.data = image

        form.populate_obj(bird)
        db.session.commit()
        flash('Bird edited successfully', 'green')
        return redirect(url_for('admin.birds', bird=bird))
    return render_template('admin/edit_bird.html', form=form, bird=bird, park_id=park_id, park_name=park_name)


@admin.route('/birds/delete/<id>', methods=['POST'])
@login_required
@admin_required
@check_confirmed
def delete_bird(id):
    bird = Bird.query.filter_by(id=id).first_or_404()
    db.session.delete(bird)
    db.session.commit()
    flash('Bird Deleted successfully', 'green')
    return redirect(url_for('admin.birds'))


@admin.route('/wildlife/view_all')
@login_required
@admin_required
def wildlife():
    allwildlife = Wildlife.query.all()

    return render_template('admin/all_wildlife.html', allwildlife=allwildlife)


@admin.route('/wildlife/add', methods=['GET', 'POST'])
@login_required
@admin_required
@check_confirmed
def add_wildlife():
    allwildlife = Wildlife.query.all()
    """Create a new bird."""
    form = AddWildlifeForm()
    form.park.choices = [(row.id, row.name) for row in Park.query.all()]
    if form.validate_on_submit():
        image = form.image.data
        if image:
            image = photos.save(form.image.data)
        park = Park.query.filter_by(id=form.park.data).first_or_404()
        newwildlife = Wildlife(
            name=form.name.data,
            description=form.description.data,
            image_url=image,
            frequency=form.frequency.data,
            park=park
        )
        db.session.add(newwildlife)
        db.session.commit()
        flash('New Wildlife created', 'green')
        return redirect(url_for('admin.wildlife'))
    return render_template('admin/new_wildlife.html', allwildlife=allwildlife, form=form)


@admin.route('/wildlife/edit/<id>', methods=('GET', 'POST'))
@login_required
@admin_required
@check_confirmed
def edit_wildlife(id):
    wildlife = Wildlife.query.filter_by(id=id).first_or_404()
    form = EditWildlifeForm(obj=wildlife)
    park_id = wildlife.park.id
    park_name = wildlife.park.name
    if form.validate_on_submit():
        image = form.image_url.data
        if image:
            image = photos.save(form.image_url.data)
            form.image_url.data = image

        form.populate_obj(wildlife)
        db.session.commit()
        flash('Wildlife edited successfully', 'green')
        return redirect(url_for('admin.wildlife', wildlife=wildlife))
    return render_template('admin/edit_wildlife.html', form=form, wildlife=wildlife, park_id=park_id, park_name=park_name)


@admin.route('/wildlife/delete/<id>', methods=['POST'])
@login_required
@admin_required
@check_confirmed
def delete_wildlife(id):
    wildlife = Wildlife.query.filter_by(id=id).first_or_404()
    db.session.delete(wildlife)
    db.session.commit()
    flash('Wildlife Deleted successfully', 'green')
    return redirect(url_for('admin.wildlife'))


@admin.route('/parks/view_all')
@login_required
@admin_required
@check_confirmed
def parks():
    allparks = Park.query.all()

    return render_template('admin/all_parks.html', allparks=allparks)


@admin.route('/parks/add', methods=['GET', 'POST'])
@login_required
@admin_required
@check_confirmed
def add_park():
    allparks = Park.query.all()
    """Create new park."""
    form = AddParkForm()
    form.country.choices = [(row.id, row.name) for row in Country.query.all()]
    if form.validate_on_submit():
        image = form.image.data
        if image:
            image = photos.save(form.image.data)
        country = Country.query.filter_by(id=form.country.data).first_or_404()
        newpark = Park(
            name=form.name.data,
            description=form.description.data,
            climate=form.climate.data,
            best_time_to_visit=form.best_time_to_visit.data,
            image_url=image,
            country=country
        )
        db.session.add(newpark)
        db.session.commit()
        flash('New Wildlife created', 'form-success')
        return redirect(url_for('admin.parks'))
    return render_template('admin/new_park.html', allparks=allparks, form=form)


@admin.route('/parks/edit/<id>', methods=('GET', 'POST'))
@login_required
@admin_required
@check_confirmed
def edit_park(id):
    park = Park.query.filter_by(id=id).first_or_404()
    form = EditParkForm(obj=park)
    country_id = park.country.id
    country_name = park.country.name
    if form.validate_on_submit():
        image = form.image_url.data
        if image:
            image = photos.save(form.image_url.data)
            form.image_url.data = image

        form.populate_obj(park)
        db.session.commit()
        flash('Park edited successfully', 'green')
        return redirect(url_for('admin.parks', park=park))
    return render_template('admin/edit_park.html', form=form, park=park, country_id=country_id, country_name=country_name)


@admin.route('/parks/delete/<id>', methods=['POST'])
@login_required
@admin_required
@check_confirmed
def delete_park(id):
    park = Park.query.filter_by(id=id).first_or_404()
    db.session.delete(park)
    db.session.commit()
    flash('Park Deleted successfully', 'green')
    return redirect(url_for('admin.parks'))


@admin.route('/settings', methods=('GET', 'POST'))
@login_required
@admin_required
def admin_settings():
    user = current_user

    return render_template('admin/settings.html', user=user)


@admin.route('/settings/change_password', methods=('GET', 'POST'))
@login_required
@admin_required
@check_confirmed
def change_password():
    """Change an existing user's password."""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.', 'green')
            return redirect(url_for('admin.settings'))
        else:
            flash('Original password is invalid.', 'red')
    return render_template('admin/change_password.html', form=form)


@admin.route('/settings/change-email', methods=['GET', 'POST'])
@admin_required
@login_required
@check_confirmed
def change_email_request():
    """Respond to existing user's request to change their email."""
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            change_email_link = url_for(
                'account.change_email', token=token, _external=True)
            get_queue().enqueue(
                send_email,
                recipient=new_email,
                subject='Confirm Your New Email',
                template='account/email/change_email',
                # current_user is a LocalProxy, we want the underlying user
                # object
                user=current_user._get_current_object(),
                change_email_link=change_email_link)
            flash('A confirmation link has been sent to {}.'.format(new_email),
                  'warning')
            return redirect(url_for('admin.settings'))
        else:
            flash('Invalid email or password.', 'form-error')
    return render_template('admin/change_email.html', form=form)


@admin.route('/settings/change-email/<token>', methods=['GET', 'POST'])
@login_required
@admin_required
@check_confirmed
def change_email(token):
    """Change existing user's email with provided token."""
    if current_user.change_email(token):
        flash('Your email address has been updated.', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'error')
    return redirect(url_for('admin.dashboard'))
