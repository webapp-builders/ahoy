from flask import Blueprint, render_template,url_for,redirect,current_app,jsonify,request
from app.models.user import User
from flask.ext.login import current_user,LoginManager,login_required,login_user,logout_user
from app.forms.event.reminder_form import ReminderForm

event = Blueprint('event', __name__)


@event.route("/event/new",methods=['GET','POST'])
@login_required
def new():
    form = ReminderForm()
    return render_template("event/new.html",form=form)


@event.route("/event/reminders")
@login_required
def reminders():
    id = current_user.id
    print "currentuser id"
    print id
    return render_template("event/reminders.html")

@event.route("/events")
@login_required
def index():
    id = current_user.id
    print "currentuser id"
    print id
    return render_template("event/reminders.html")

@event.route("/events/<int:id>")
@login_required
def details():
    id = current_user.id
    print "currentuser id"
    print id
    return render_template("event/reminders.html")
