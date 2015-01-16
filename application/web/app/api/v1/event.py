from flask import Blueprint, render_template,url_for,redirect,jsonify
from app import app


event = Blueprint('event_v1', __name__)

#/api/v1/events
@event.route("/events")
def index():
    return jsonify({"events":[]})
