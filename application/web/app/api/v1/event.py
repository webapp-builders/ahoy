from flask import Blueprint, render_template,url_for,redirect,current_app,jsonify


event = Blueprint('event_v1', __name__)#url_prefix='/api/v1'

@event.route("/events")
def index():
    return jsonify({"events":[]})
