from flask import Blueprint, render_template,url_for,redirect
from app import app

account = Blueprint('account', __name__)

@account.route("/signup")
def signup():
    return render_template("account/signup.html",page="account signup")


@account.route("/signin")
def signin():
    return render_template("account/signin.html",page="account signin")
