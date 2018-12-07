from flask import render_template, current_app, url_for
from flask_babel import _
from app.email1 import send_email



def send_password_reset_email(user):
    token = user.generate_password_reset_token()
    send_email(_('[Safari] Reset Your Password'),
               sender='noreply@out2safari.com',
               recipients=[user.email],
               text_body=render_template('account/email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('account/email/reset_password.html',
                                         user=user, token=token))


def send_confirm_email(user):
    token =user.get_confirmation_token()
    confirm_link = url_for('account.confirm', token=token, _external=True)
    send_email(_('[Safari] Confirm Your Account'),
               sender='noreply@out2safari.com',
               recipients=[user.email],
               text_body=render_template('account/email/confirm.txt',
                                         user=user, confirm_link=confirm_link),
               html_body=render_template('account/email/confirm.html',
                                         user=user, confirm_link=confirm_link))
