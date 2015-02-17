from flask import Blueprint, render_template,url_for,redirect,current_app,jsonify,request,flash
from flask.ext.login import login_user,current_user,logout_user
from itsdangerous import URLSafeTimedSerializer
import uuid
from app.forms.account.signin_form import SigninForm
from app.forms.account.signup_form import SignupForm
from app.forms.account.email_form import EmailForm
from app.models.user import User
from app.mailers import account_mailer
from app.helpers import account_helper

account = Blueprint('account', __name__)

"""
signup and account verification feature  responders
"""

@account.route('/account/signup',methods=['POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username, email, token = User.signup(form)
        verification_url = url_for('account.verify',email=email,token=token,_external=True)
        account_mailer.send_account_verification_email(username=username,email=email,url=verification_url)
        if current_app.debug:
            return redirect(url_for('account.created',url=verification_url))
        return redirect(url_for('account.created'))
    return render_template("home/index.html",form=form)



@account.route('/account/verification',methods=['GET','POST'])
def send_verification_email():
    form = EmailForm()
    if form.validate_on_submit():
        user= User.validate(form.email.data)
        if user:
            if not user.verified:
                verification_url = url_for('account.verify',email=user.email,token=user.verification_token,_external=True)
                account_mailer.send_account_verification_email(username=user.username,email=user.email,url=verification_url)
                if current_app.debug:
                    return redirect(url_for('account.created',url=verification_url))
                return redirect(url_for('account.created'))
            else:
                flash("account is already verified. you may signin to your account")
                return redirect(url_for('account.signin'))
        else:
            flash("User not found. Is the email you entered correct?")
    return render_template("account/send_token.html",form=form)


@account.route('/account/created')
def created():
    return render_template("account/created.html",url=request.args.get('url') or "#",debug=current_app.debug)


@account.route('/account/verify')
def verify():
    user = User.account_verified(request)
    if user and user.is_active():
        login_user(user, remember=True)
        return redirect(url_for('event.new'))
    account_helper.flash_failed_account_verification_messages(user)
    return redirect(url_for('account.send_verification_email'))

"""
signin\signout feature responders
"""

@account.route("/account/signin",methods=['GET','POST'])
def signin():
    if current_user.is_authenticated():
        return redirect(url_for('home.index'))
    form = SigninForm()
    if form.validate_on_submit():
        user = User.signin(form)
        if user:
            if not user.verified:
                verification_url = url_for('account.verify',email=user.email,token=user.verification_token,_external=True)
                account_mailer.send_account_verification_email(username=user.username,email=user.email,url=verification_url)
                if current_app.debug:
                    return redirect(url_for('account.created',url=verification_url))
                return redirect(url_for('account.created'))
            if user.is_active():
                login_user(user, remember=True)
                return_url = request.form.get('next')
                return redirect(request.form.get('next') or url_for('event.reminders'))
        account_helper.flash_failed_messages(user)
    return render_template("account/signin.html",form=form)


@account.route('/account/signout')
def signout():
    current_user.authenticated = False
    logout_user()
    return redirect(url_for('home.index'))


"""
Password reset feature responders
"""

@account.route('/account/password',methods=['GET','POST'])
def send_password_email():
    form = EmailForm()
    if form.validate_on_submit():
        user = User.refresh_password_reset_token(form.email.data)
        if user:
            if not user.banned:
                #note: dont care if user is not verified because password reset will also verify the user
                verification_url = url_for('account.reset_password',email=user.email,token=user.password_reset_token,_external=True)
                account_mailer.send_password_reset_email(username=user.username,email=user.email,url=verification_url)
                if current_app.debug:
                    return redirect(url_for('account.password_reset_sent',url=verification_url))
                return redirect(url_for('account.password_reset_sent'))
            else:
                flash("Your account has been suspended for the following reason")
                flash(user.reason)
                flash("Please contact us, if you belive this is in error")
                return redirect(url_for('home.index'))
        else:
            flash("User not found. Is the email you entered correct?")
    return render_template("account/forgot_password.html",form=form)


@account.route('/account/sent')
def password_reset_sent():
    return render_template("account/password_email_sent.html",url=request.args.get('url') or "#",debug=current_app.debug)


@account.route('/account/reset',methods=['GET','POST'])
def reset_password():
    email=request.args.get('email')
    form = SigninForm(email=email)
    if form.validate_on_submit():
        user = User.reset_password(form,request)
        if user:
            if user.is_active():
                login_user(user, remember=True)
                return redirect(url_for('event.reminders'))
        account_helper.flash_failed_reset_password_messages(user)
    return render_template("account/reset_password.html",form=form)



