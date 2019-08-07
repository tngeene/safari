from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    jsonify,
    request,
    send_from_directory,
)
from flask_login import current_user, login_required, logout_user
from app.auth.admin_decorators import publisher_login_required, check_profile
from app.publisher.forms import *
import os, random, string, PIL, simplejson, traceback
from PIL import Image
from werkzeug import secure_filename
from app.lib.upload_file import uploadfile
from app.auth.email import send_operator_registered

publisher = Blueprint("publisher", __name__)
photos = UploadSet("photos", IMAGES)

from app.publisher.countries import get_countries, get_arcode

ALLOWED_EXTENSIONS = set(
    ["txt", "gif", "png", "jpg", "jpeg", "bmp", "rar", "zip", "7zip", "doc", "docx"]
)


@publisher.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@publisher.route("/")
@login_required
@publisher_login_required
@check_profile
def dashboard():
    """Admin dashboard page."""
    listing_count = current_user.listings.count()
    booking_count = current_user.bookings_count()
    destination_count = current_user.listings.group_by(Listing.location).count()
    bookings = (
        Booking.query.join(Listing, (Listing.id == Booking.listing_id))
        .filter(Listing.publisher_id == current_user.id)
        .order_by(Booking.createdAt.desc())
        .limit(5)
    )

    cancelled = (
        Booking.query.join(Listing, (Listing.id == Booking.listing_id))
        .filter(Listing.publisher_id == current_user.id, Booking.state == "cancelled")
        .order_by(Booking.createdAt.desc())
        .limit(5)
    )
    return render_template(
        "publisher/index.html",
        listing_count=listing_count,
        booking_count=booking_count,
        destination_count=destination_count,
        bookings=bookings,
        cancelled=cancelled,
    )


@publisher.route("/listings/<country>")
@login_required
@publisher_login_required
@check_profile
def listing(country):
    listings = (
        Listing.query.filter_by(publisher=current_user, location=country)
        .order_by(Listing.createdAt.desc())
        .all()
    )
    return render_template("publisher/listing.html", items=listings, country=country)


@publisher.route("/listings/new", methods=("GET", "POST"))
@login_required
@publisher_login_required
@check_profile
def newListing():
    form = ListingForm()
    form.categories.choices = [
        (row.id, row.name)
        for row in Category.query.order_by(Category.createdAt.desc()).all()
    ]
    form.categories.choices.insert(0, (0, "--Select Category--"))
    form.location.choices = get_countries()
    if form.validate_on_submit():
        listing = Listing(
            title=form.title.data,
            location=form.location.data,
            duration=form.duration.data,
            availability_from=form.availability_from.data,
            availability_to=form.availability_to.data,
            physical_condition=form.physical_condition.data,
            package=form.package.data,
            connectivity=form.connectivity.data,
            publisher=current_user,
        )

        for row in form.categories.data:
            category = Category.query.filter_by(id=row).first_or_404()
            listing.categories.append(category)

        db.session.add(listing)
        db.session.commit()
        return redirect(url_for("publisher.newPricing", id=listing.id))
    return render_template("publisher/add_listing.html", form=form)


@publisher.route("/listings/edit/<id>", methods=("GET", "POST"))
@login_required
@publisher_login_required
@check_profile
def editListing(id):
    listing = Listing.query.filter_by(id=id, publisher=current_user).first_or_404()
    form = ListingForm(obj=listing)
    form.location.choices = get_countries()
    form.categories.choices = [
        (row.id, row.name)
        for row in Category.query.order_by(Category.createdAt.desc()).all()
    ]
    form.categories.choices.insert(0, (0, "--Select Category--"))
    if form.validate_on_submit():
        listing.title = (form.title.data,)
        listing.location = (form.location.data,)
        listing.duration = (form.duration.data,)
        listing.availability_from = (form.availability_from.data,)
        listing.availability_to = (form.availability_to.data,)
        listing.physical_condition = (form.physical_condition.data,)
        listing.package = (form.package.data,)
        listing.connectivity = form.connectivity.data
        for category in listing.categories:
            listing.categories.remove(category)
        db.session.commit()

        for row in form.categories.data:
            category = Category.query.filter_by(id=row).first_or_404()
            listing.categories.append(category)
        return redirect(url_for("publisher.newPricing", id=listing.id))
    return render_template("publisher/add_listing.html", form=form, listing=listing)


@publisher.route("/listings/delete/<id>", methods=["POST"])
@login_required
@publisher_login_required
@check_profile
def deleteListing(id):
    listing = Listing.query.filter_by(id=id, publisher=current_user).first_or_404()
    db.session.delete(listing)
    db.session.commit()
    flash("Listing Deleted successfully", "green")
    return redirect(url_for("publisher.listing", country=listing.location))


@publisher.route("/listings/publish/<id>")
@login_required
@publisher_login_required
@check_profile
def publishListing(id):
    listing = Listing.query.filter_by(id=id, publisher=current_user).first_or_404()
    if listing.published == True:
        listing.published = False
    else:
        listing.published = True
    db.session.commit()
    flash("Listing Published", "green")
    return redirect(url_for("publisher.listing", country=listing.location))


@publisher.route("/category")
@login_required
@check_profile
def category():
    categories = Category.query.order_by(Category.createdAt.desc()).all()
    return render_template("publisher/category.html", items=categories)


@publisher.route("/category/new", methods=("GET", "POST"))
@login_required
@check_profile
def newCategory():
    form = CategoryForm()
    if form.validate_on_submit():
        image = form.image.data
        if image:
            image = photos.save(form.image.data)
        category = Category(name=form.name.data, image_url=image)
        db.session.add(category)
        db.session.commit()
        flash("Category added successfully", "green")
        return redirect(url_for("publisher.category"))
    return render_template("publisher/add_category.html", form=form)


@publisher.route("/destinations")
@login_required
@publisher_login_required
@check_profile
def destination():
    destinations = Listing.query.filter_by(publisher=current_user).group_by(
        Listing.location
    )
    return render_template("publisher/destination.html", items=destinations)


@publisher.route("/packages")
@login_required
@publisher_login_required
@check_profile
def package():
    pricing = Price.query.filter_by(publisher=current_user).group_by(Price.location)
    arcodes = get_arcode()
    return render_template("publisher/package.html", items=pricing, arcodes=arcodes)


@publisher.route("/packages/<country>")
@login_required
@publisher_login_required
@check_profile
def pricing(country):
    pricing = (
        Price.query.filter_by(publisher=current_user, location=country)
        .order_by(Price.createdAt.desc())
        .all()
    )
    return render_template("publisher/pricing.html", items=pricing, country=country)


@publisher.route("/pricing/new/<id>", methods=("GET", "POST"))
@login_required
@publisher_login_required
@check_profile
def newPricing(id):
    listing = Listing.query.filter_by(id=id, publisher=current_user).first_or_404()
    form = PriceForm(obj=listing.price)
    if form.validate_on_submit():
        if not listing.price:
            price = Price(
                total_price_adults=form.total_price_adults.data,
                total_price_children=form.total_price_children.data,
                price_per_day_adults=form.price_per_day_adults.data,
                price_per_day_children=form.price_per_day_children.data,
                listing=listing,
                publisher=current_user,
            )
            db.session.add(price)
            for item in form.includes.data:
                includes = Include(include=item["include"], price=price)
                db.session.add(includes)
        else:
            form.populate_obj(listing.price)
        db.session.commit()
        return redirect(url_for("publisher.newExtras", id=listing.id))
    return render_template("publisher/add_price.html", form=form, listing=listing)


@publisher.route("/pricing/edit/<id>", methods=("GET", "POST"))
@login_required
@publisher_login_required
@check_profile
def editPricing(id):
    pricing = Price.query.filter_by(id=id).first_or_404()
    form = EditPriceForm(obj=pricing)
    form.location.choices = get_countries()
    if form.validate_on_submit():
        form.populate_obj(pricing)
        db.session.commit()
        flash("Pricing edited successfully", "green")
        return redirect(url_for("publisher.pricing", country=pricing.location))
    return render_template("publisher/add_price.html", form=form)


@publisher.route("/extras/new/<id>", methods=("GET", "POST"))
@login_required
@publisher_login_required
@check_profile
def newExtras(id):
    listing = Listing.query.filter_by(id=id, publisher=current_user).first_or_404()
    form = ExtrasForm(obj=listing)
    if form.validate_on_submit():
        form.populate_obj(listing)
        db.session.commit()
        return redirect(url_for("publisher.newPolicy", id=listing.id))
    return render_template("publisher/add_extra.html", form=form, listing=listing)


@publisher.route("/policy/new/<id>", methods=("GET", "POST"))
@login_required
@publisher_login_required
@check_profile
def newPolicy(id):
    listing = Listing.query.filter_by(id=id, publisher=current_user).first_or_404()
    form = PolicyForm(obj=listing)
    if form.validate_on_submit():
        form.populate_obj(listing)
        db.session.commit()
        return redirect(url_for("publisher.newImages", id=listing.id))
    return render_template("publisher/add_policy.html", form=form, listing=listing)


@publisher.route("/images/new/<id>", methods=("GET", "POST"))
@login_required
@publisher_login_required
@check_profile
def newImages(id):
    listing = Listing.query.filter_by(id=id, publisher=current_user).first_or_404()
    form = ImageForm()
    if form.validate_on_submit():
        for image in listing.images:
            db.session.delete(image)

        for image in form.images.data:
            if image["image"] is not None:
                img = photos.save(image["image"])
                image = Image(image_url=img, listing=listing)
                db.session.add(image)
        db.session.commit()
        return redirect(url_for("publisher.listing", country=listing.location))
    return render_template("publisher/add_image.html", form=form, listing=listing)


@publisher.route("/bookings")
@login_required
@publisher_login_required
@check_profile
def bookings():
    current_user.last_booking_read_time = datetime.utcnow()
    current_user.add_notification("unread_booking_count", 0)
    db.session.commit()
    bookings = (
        Booking.query.join(Listing, (Listing.id == Booking.listing_id))
        .filter(Listing.publisher_id == current_user.id)
        .order_by(Booking.createdAt.desc())
        .all()
    )
    return render_template("publisher/bookings.html", bookings=bookings)


@publisher.route("/confirm_booking/<id>/<state>")
@login_required
@publisher_login_required
@check_profile
def confirm_booking(id, state):
    booking = Booking.query.filter_by(id=id).first_or_404()
    if booking.listing.publisher != current_user:
        return redirect(url_for("home.index"))
    booking.state = state
    db.session.commit()
    flash("Status Updated", "green")
    return redirect(url_for("publisher.bookings"))


@publisher.route("/cancel_booking", methods=["POST"])
@login_required
@publisher_login_required
@check_profile
def cancel_booking():
    id = request.args.get("id", 0, type=int)
    if request.method == "POST":
        booking = Booking.query.filter_by(id=id).first_or_404()
        if booking.listing.publisher != current_user:
            return 401
        booking.state = "cancelled"
        booking.reason = request.form.get("reason")
        db.session.commit()
    bookings = (
        Booking.query.join(Listing, (Listing.id == Booking.listing_id))
        .filter(Listing.publisher_id == current_user.id)
        .order_by(Booking.createdAt.desc())
        .all()
    )
    return render_template("publisher/_bookings.html", bookings=bookings)


@publisher.route("/send_message/<id>", methods=["GET", "POST"])
@login_required
@check_profile
def send_message(id):
    user = User.query.filter_by(id=id).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user, body=form.message.data)
        db.session.add(msg)
        user.add_notification("unread_message_count", user.new_messages())
        db.session.commit()
        flash("Your message has been sent.", "green")
        return redirect(url_for("publisher.messages"))
    return render_template(
        "publisher/send_message.html", title="Send Message", form=form, user=user
    )


@publisher.route("/messages")
@login_required
@check_profile
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification("unread_message_count", 0)
    db.session.commit()
    page = request.args.get("page", 0, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()
    ).group_by(Message.sender_id)
    return render_template("publisher/messages.html", messages=messages)


@publisher.route("/notifications")
@login_required
@check_profile
def notifications():
    since = request.args.get("since", 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since
    ).order_by(Notification.timestamp.asc())
    return jsonify(
        [
            {"name": n.name, "data": n.get_data(), "timestamp": n.timestamp}
            for n in notifications
        ]
    )


@publisher.route("/notifications_view")
@login_required
@check_profile
def notifications_view():
    bookings = current_user.user_notifications()
    return render_template("publisher/_notification.html", notifications=bookings)


@publisher.route("/settings", methods=["GET", "POST"])
@login_required
@check_profile
def settings():
    form = EditPasswordForm()
    if form.validate_on_submit():
        current_user.password = form.password.data
        db.session.commit()
        flash("Password changed successfully", "green")
        return redirect(url_for("publisher.settings"))
    return render_template("publisher/settings.html", form=form, title="Edit Password")


@publisher.route("/profile")
@login_required
@publisher_login_required
@check_profile
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
        flash("Category added successfully", "green")
        return redirect(url_for("publisher.category"))
    return render_template("publisher/profile.html", form=form)


@publisher.route("/view_profile/<id>")
@login_required
@publisher_login_required
@check_profile
def get_profile(id):
    user = User.query.get_or_404(id)
    return render_template("publisher/_profile_modal.html", user=user)


@publisher.route("/edit_profile", methods=("GET", "POST"))
@login_required
@publisher_login_required
def edit_profile():
    form = ProfileForm()
    publisher = current_user.publisher
    if publisher is not None:
        form = EditProfileForm(obj=publisher)
    if form.validate_on_submit():
        if publisher is not None:
            new_registration = False
            form.operator_licence.data = photos.save(form.operator_licence.data)
            form.reg_certificate.data = photos.save(form.reg_certificate.data)
            form.tax_registration.data = photos.save(form.tax_registration.data)
            form.populate_obj(publisher)
        else:
            new_registration = True
            operator_licence = photos.save(form.operator_licence.data)
            reg_certificate = photos.save(form.reg_certificate.data)
            tax_registration = photos.save(form.tax_registration.data)
            profile = Publisher(
                company_name=form.company_name.data,
                overview=form.overview.data,
                physical_address=form.physical_address.data,
                postal_address=form.postal_address.data,
                association_membership=form.association_membership.data,
                user=current_user,
                operator_licence=operator_licence,
                reg_certificate=reg_certificate,
                tax_registration=tax_registration,
                bank_name=form.bank_name.data,
                bank_account=form.bank_account.data,
                swift_code=form.swift_code.data,
                director=form.director.data,
                director_phone=form.director_phone.data,
                director_email=form.director_email.data,
            )

            for item in form.phones.data:
                phones = Pubphones(phone_number=item["phone_number"], profile=profile)
                db.session.add(phones)

            for item in form.emails.data:
                emails = Pubemails(email=item["email"], profile=profile)
                db.session.add(emails)

            for item in form.locations.data:
                locations = Publocations(
                    city=item["city"], country=item["country"], profile=profile
                )
                db.session.add(locations)
            db.session.add(profile)
        db.session.commit()
        if new_registration:
            send_operator_registered(publisher)
        flash("Profile Edited successfully waiting for Adminstrator approval", "green")
        return redirect(url_for("publisher.edit_cover"))
    return render_template("publisher/edit_profile.html", form=form)


@publisher.route("/edit_cover", methods=("GET", "POST"))
@login_required
@publisher_login_required
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
        flash("Cover Added successfully waiting for Adminstrator approval", "green")
        return redirect(url_for("publisher.profile"))
    return render_template("publisher/edit_cover.html", form=form)


@publisher.route("/_get_pricing/")
def _get_pricing():
    location = request.args.get("location", "01", type=str)
    pricing = [
        (row.id, row.name)
        for row in Price.query.filter_by(location=location)
        .order_by(Price.createdAt.desc())
        .all()
    ]
    return jsonify(pricing)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def gen_file_name(filename):
    """
    If file was exist already, rename it and return a new name
    """

    i = 1
    while os.path.exists(os.path.join(current_app.config["UPLOAD_FOLDER"], filename)):
        name, extension = os.path.splitext(filename)
        filename = "%s_%s%s" % (name, str(i), extension)
        i += 1

    return filename


def create_thumbnail(image):
    try:
        base_width = 100
        img = Image.open(os.path.join(current_app.config["UPLOAD_FOLDER"], image))
        w_percent = base_width / float(img.size[0])
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((base_width, h_size), PIL.Image.ANTIALIAS)
        img.save(os.path.join(current_app.config["THUMBNAIL_FOLDER"], image))

        return True

    except:
        print(traceback.format_exc())
        return False


@publisher.route("/upload/<p_table>/<c_table>/<id>", methods=["GET", "POST"])
def upload(p_table, c_table, id):
    if request.method == "POST":
        files = request.files["file"]

        if files:
            filename = secure_filename(files.filename)
            filename = gen_file_name(filename)
            mime_type = files.content_type
            p_model = User.get_class_by_tablename(p_table)

            if not allowed_file(files.filename):
                result = uploadfile(
                    name=filename,
                    table=c_table,
                    type=mime_type,
                    size=0,
                    not_allowed_msg="File type not allowed",
                )

            else:
                # save file to disk
                uploaded_file_path = os.path.join(
                    current_app.config["UPLOAD_FOLDER"], filename
                )
                files.save(uploaded_file_path)
                p_model = User.get_class_by_tablename(p_table)
                c_model = User.get_class_by_tablename(c_table)
                parent_table = p_model.query.filter_by(id=id).first_or_404()
                if parent_table.images.count() >= 5:
                    return "You cannot add more than 5 images", 400
                new_image = c_model(image_url=filename, listing_id=parent_table.id)
                db.session.add(new_image)
                db.session.commit()

                # create thumbnail after saving
                if mime_type.startswith("image"):
                    create_thumbnail(filename)

                # get file size after saving
                size = os.path.getsize(uploaded_file_path)

                # return json for js call back
                result = uploadfile(
                    name=filename, table=c_table, type=mime_type, size=size
                )

            return simplejson.dumps({"files": [result.get_file()]})

    if request.method == "GET":
        # get all file in ./data directory
        p_model = User.get_class_by_tablename(p_table)
        c_model = User.get_class_by_tablename(c_table)
        parent_table = p_model.query.filter_by(id=id).first_or_404()
        files = [
            f.image_url
            for f in c_model.query.filter_by(listing_id=parent_table.id).all()
            if os.path.isfile(
                os.path.join(current_app.config["UPLOAD_FOLDER"], f.image_url)
            )
        ]
        file_display = []

        for f in files:
            size = os.path.getsize(os.path.join(current_app.config["UPLOAD_FOLDER"], f))
            file_saved = uploadfile(name=f, size=size, table=c_table)
            file_display.append(file_saved.get_file())

        return simplejson.dumps({"files": file_display})

    return redirect(url_for("index"))


@publisher.route("/delete_image/<table>/<string:filename>", methods=["DELETE"])
def delete_image(table, filename):
    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file_thumb_path = os.path.join(current_app.config["THUMBNAIL_FOLDER"], filename)
    c_model = User.get_class_by_tablename(table)
    table = c_model.query.filter_by(image_url=filename).first_or_404()
    db.session.delete(table)
    db.session.commit()
    if os.path.exists(file_path):
        try:
            os.remove(file_path)

            if os.path.exists(file_thumb_path):
                os.remove(file_thumb_path)

            return simplejson.dumps({filename: "True"})
        except:
            return simplejson.dumps({filename: "False"})


# serve static files
@publisher.route("/thumbnail/<string:filename>", methods=["GET"])
def get_thumbnail(filename):
    return send_from_directory(
        current_app.config["THUMBNAIL_FOLDER"], filename=filename
    )


@publisher.route("/data/<string:filename>", methods=["GET"])
def get_file(filename):
    return send_from_directory(
        os.path.join(current_app.config["UPLOAD_FOLDER"]), filename=filename
    )
