from flask import Blueprint, render_template,url_for,redirect
from app import app


home = Blueprint('home', __name__)


@home.route("/")
def index():
    return render_template("home/index.html",page="home index")
