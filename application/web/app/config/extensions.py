from flask import redirect,url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.uuid import FlaskUUID
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask.ext.moment import Moment
from flask_debugtoolbar import DebugToolbarExtension

#all application plugins that can be imported from this module
db = SQLAlchemy()
flaskuuid = FlaskUUID()
bcrypt = Bcrypt()
login_manager = LoginManager()
moment = Moment()
debug_toolbar = DebugToolbarExtension()

#initilalize the plugins in this method
#which is called from the factory method creates the flask application
def initialize_extensions(app):
    db.init_app(app)
    flaskuuid.init_app(app)
    bcrypt.init_app(app)
    moment.init_app(app)
    debug_toolbar.init_app(app)

    #flask-login initialization
    from app.models.user import load_user
    #comment this line to use the default flask login login view functionality
    login_manager.login_view =  "account.signin"
    login_manager.session_protextion =  "strong"
    login_manager.init_app(app)
    login_manager.user_loader(load_user)



#un-comment this function to use the explicit flask login login view functionality
# @login_manager.unauthorized_handler
# def unauthorized():
#     return redirect(url_for("home.index"))

# from app.models.user import load_user
# @login_manager.user_loader
# def load_user(user_id):
#     print "user_loader"
#     return User()



