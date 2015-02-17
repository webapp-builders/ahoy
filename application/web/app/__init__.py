from flask import Flask, g
from functools import wraps
import datetime

#from flask_failsafe import failsafe
#@failsafe
def create_app(settings=None):

    #create the flask application
    app = Flask(__name__)

    #configure flask application before initializing application extensions
    if settings is None:
        from app.config.settings import Settings
        app.config.from_object(Settings())
    else:
        app.config.from_object(settings)

    #configure flask application extensions
    from app.config.extensions import initialize_extensions
    initialize_extensions(app)

    #configure url routing rules before registering application blueprints
    from app.config.routes import add_url_rules
    add_url_rules(app)

    #register application blueprints (i.e. register responders)
    from app.config.blueprints import register_blueprints
    register_blueprints(app)

    #register global application error handlers
    from app.config.handlers import register_error_handlers
    register_error_handlers(app)

    #register global per request filters
    from app.config.request_filters import register_per_request_filters
    register_per_request_filters(app)

    #configure jinja template filters
    from app.config.jinja_filters import register_jinja_filters
    register_jinja_filters(app)


    from app.config.loggers import register_loggers
    register_loggers(app)

    return app








