from flask import Blueprint, render_template,url_for,redirect,current_app,jsonify,request
from app.models.user import User
from flask.ext.login import current_user,LoginManager,login_required,login_user,logout_user
from app.forms.event.reminder_form import ReminderForm

demo = Blueprint('demo', __name__)

#@demo.route("/event/new")
@demo.route("/demo/how")
def how():
    form = ReminderForm()
    return render_template("demo/how.html",form=form)



