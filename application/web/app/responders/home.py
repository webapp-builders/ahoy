from flask import Blueprint, render_template,url_for,redirect,current_app,jsonify,request
from app.forms.account.signup_form import SignupForm
#from app.forms.event.reminder_form import ReminderForm
from flask.ext.login import login_user,current_user

home = Blueprint('home', __name__)

@home.route("/")
def index():
    # form = SignupForm()
    # return render_template("home/index.html",form=form)
    if current_user.is_authenticated():
        # form = AddEventForm()
        # return render_template("event/new.html",form=form)
        return render_template("event/reminders.html")
    else:
        form = SignupForm()
        return render_template("home/index.html",form=form)





