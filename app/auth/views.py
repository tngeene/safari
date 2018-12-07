from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_rq import get_queue

from app import db
from app.auth.forms import (
    ChangeEmailForm,
    ChangePasswordForm,
    CreatePasswordForm,
    LoginForm,
    RegistrationForm,
    RequestResetPasswordForm,
    ResetPasswordForm,
)

import httplib2

from app.email import send_email
from app.models import User
from app.customer.forms import *
from app.auth.email import send_confirm_email
from app.auth.email import send_password_reset_email
#from oauth import OAuthSignIn


account = Blueprint('account', __name__)


@account.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('home.index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@account.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('home.index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('home.index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    if current_user.role.index == 'admin':
        return redirect(request.args.get('next') or url_for('admin.dashboard'))
    elif current_user.role.index == 'publisher':
        return redirect(request.args.get('next') or url_for('publisher.dashboard'))
    else:
        return redirect(request.args.get('next') or url_for('customer.dashboard'))


@account.route('/', methods=['GET', 'POST'])
def login():
    """Log in an existing user."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.password_hash is not None and \
                user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('You are now logged in. Welcome!', 'green')
            if current_user.role.index == 'admin':
                return redirect(request.args.get('next') or url_for('admin.dashboard'))
            elif current_user.role.index == 'publisher':
                return redirect(request.args.get('next') or url_for('publisher.dashboard'))
            else:
                return redirect(request.args.get('next') or url_for('customer.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('home/login.html', form=form)
    # return render_template('account/user-login.html', form=form)


@account.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user, and send them a confirmation email."""
    form = RegistrationForm()
    if form.validate_on_submit():
        role = Role.query.filter_by(index='customer').first_or_404()
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data, role=role)

        db.session.add(user)
        db.session.commit()
        send_confirm_email(user)
        login_user(user, False)
        return redirect(url_for('account.unconfirmed'))
    return render_template('home/register.html', form=form)


@account.route('register/publisher', methods=['GET', 'POST'])
def register_publisher():
    # Register an new publisher and send them a confirmation email
    form = RegistrationForm()
    if form.validate_on_submit():
        role = Role.query.filter_by(index='publisher').first_or_404()
        user = User(
            first_name=form.first_name.data,
            last_name = form.last_name.data,
            email = form.email.data,
            password = form.password.data, role=role)
        db.session.add(user)
        db.session.commit()

        send_confirm_email(user)
        login_user(user)
        return redirect(url_for('account.unconfirmed'))
    return render_template('home/register.html', form=form)


@account.route('/logout')
@login_required
def logout():
    logout_user()
    # Delete the user's profile and the credentials stored by oauth2.
    return redirect(url_for('home.index'))


@account.route('/manage', methods=['GET', 'POST'])
@account.route('/manage/info', methods=['GET', 'POST'])
@login_required
def manage():
    """Display a user's account information."""
    return render_template('account/manage.html', user=current_user, form=None)


@account.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    """Respond to existing user's request to reset their password."""
    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('A password reset link has been sent to {}.'.format(
            form.email.data), 'warning')
        return redirect(url_for('account.login'))
    return render_template('home/reset_password.html', form=form)


@account.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset an existing user's password."""

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('Invalid email address.', 'form-error')
            return redirect(url_for('home.index'))
        if user.reset_password(token, form.new_password.data):
            flash('Your password has been updated.', 'success')
            return redirect(url_for('account.login'))
        else:
            flash('The password reset link is invalid or has expired.',
                  'error')
            return redirect(url_for('home.index'))
    return render_template('home/reset_password2.html', form=form, token=token)


@account.route('/manage/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change an existing user's password."""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.', 'form-success')
            return redirect(url_for('main.index'))
        else:
            flash('Original password is invalid.', 'form-error')
    return render_template('account/manage.html', form=form)


@account.route('/manage/change-email', methods=['GET', 'POST'])
@login_required
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
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.', 'form-error')
    return render_template('account/manage.html', form=form)


@account.route('/manage/change-email/<token>', methods=['GET', 'POST'])
@login_required
def change_email(token):
    """Change existing user's email with provided token."""
    if current_user.change_email(token):
        flash('Your email address has been updated.', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'error')
    return redirect(url_for('main.index'))


@account.route('/confirm-account')
@login_required
def confirm_request():
    """Respond to new user's request to confirm their account."""
    send_confirm_email(current_user)
    flash('A new confirmation link has been sent to {}.'.format(
        current_user.email), 'green')
    return redirect(url_for('account.unconfirmed'))


@account.route('/confirm-account/<token>')
@login_required
def confirm(token):
    """Confirm new user's account with provided token."""
    if current_user.confirmed:
        if current_user.role_id == 2:
            flash('Your account has been confirmed.', 'green')
            return redirect(url_for('customer.dashboard'))
        elif current_user.role_id == 3:
            flash('Your account has been confirmed, Please finish your Registration.', 'cyan')
            return redirect(url_for('publisher.edit_profile'))
        return redirect(url_for('account.login'))
    if User.check_token(token):
        user=User.check_token(token)
        user.confirmed = True
        db.session.commit()

        # login_user(user)
        if user.role_id == 2:
            flash('Your account has been confirmed.', 'green')
            return redirect(url_for('customer.dashboard'))
        elif user.role_id == 3:
            flash('Your account has been confirmed.', 'green')
            return redirect(url_for('publisher.dashboard'))
        return redirect(url_for('account.login'))
    else:
        flash('The confirmation link is invalid or has expired.', 'red')
    return redirect(url_for('account.unconfirmed'))


@account.route(
    '/join-from-invite/<int:user_id>/<token>', methods=['GET', 'POST'])
def join_from_invite(user_id, token):
    """
    Confirm new user's account with provided token and prompt them to set
    a password.
    """
    if current_user is not None and current_user.is_authenticated:
        flash('You are already logged in.', 'error')
        return redirect(url_for('main.index'))

    new_user = User.query.get(user_id)
    if new_user is None:
        return redirect(404)

    if new_user.password_hash is not None:
        flash('You have already joined.', 'error')
        return redirect(url_for('main.index'))

    if new_user.confirm_account(token):
        form = CreatePasswordForm()
        if form.validate_on_submit():
            new_user.password = form.password.data
            db.session.add(new_user)
            db.session.commit()
            flash('Your password has been set. After you log in, you can '
                  'go to the "Your Account" page to review your account '
                  'information and settings.', 'success')
            return redirect(url_for('account.login'))
        return render_template('account/join_invite.html', form=form)
    else:
        flash('The confirmation link is invalid or has expired. Another '
              'invite email with a new link has been sent to you.', 'error')
        token = new_user.generate_confirmation_token()
        invite_link = url_for(
            'account.join_from_invite',
            user_id=user_id,
            token=token,
            _external=True)
        get_queue().enqueue(
            send_email,
            recipient=new_user.email,
            subject='You Are Invited To Join',
            template='account/email/invite',
            user=new_user,
            invite_link=invite_link)
    return redirect(url_for('main.index'))


# @account.before_app_request
# def before_request():
#     """Force user to confirm email before accessing login-required routes."""
#     if current_user.is_authenticated \
#             and not current_user.confirmed \
#             and request.endpoint[:8] != 'account.' \
#             and request.endpoint != 'static':
#         return redirect(url_for('account.unconfirmed'))


@account.route('/unconfirmed')
def unconfirmed():
    """Catch users with unconfirmed emails."""
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('home.index'))
    return render_template('account/unconfirmed.html')
