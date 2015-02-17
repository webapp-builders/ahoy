
from flask import url_for,current_app,flash
from itsdangerous import URLSafeTimedSerializer
from app.models.user import User
import uuid


def flash_failed_account_verification_messages(user):
    if user is None:
        flash("user not found")
        return
    flash("account verification failed due to invalid or expired token")
    flash("please enter the account email to receive a new account verification email")
    return

def flash_failed_messages(user):
    if user is None:
        flash("invalid username or password")
        return
    if not user.verified:
        #account_mailer.queue_account_verifcation_email(username,email,generate_verification_token())
        flash("use account not verified. check your email for a verification link")
        return
    if user.banned:
        flash("use account was banned for the following reason:")
        flash(user.reason)
        flash("please contact us if you believe your account was banned due to an error")
        return
    if user.lockedout:
        flash("your account signin was locked out temporarily due to excessive invalid signin attempts")
        flash("please wait fifteen minutes before attempting to sign in again")
        flash("or use the forgot password link to set new password")
        return
    #default: user.authenticated==False response
    flash("invalid username or password")
    return

def flash_failed_reset_password_messages(user):
    if user is None:
        flash("user not found")
        return
    if user.banned:
        flash("use account was banned for the following reason:")
        flash(user.reason)
        flash("please contact us if you believe your account was banned due to an error")
        return
    #default: user.authenticated==False response
    return "token invalid or expired. Please send a new password request email"


def valid_uuid(token):
    try:
        val = uuid.UUID(token, version=4)
    except ValueError:
        return False
    #so far we tested that the token is a valid hex string but
    #since UUID will silently convert the non uuid4 hex token string to a uuid4 hex string
    #so we check to see if the input string was converted and if so we still return false
    return val.hex == token


def create_safe_token():
    secret = current_app.config["SECRET_KEY"]
    ts = URLSafeTimedSerializer(secret)
    token=ts.dumps(email, salt=secret)
    return token


# def add_flash_messages(messages_array):
    #     for message in messages_array:
    #         flash(message)

