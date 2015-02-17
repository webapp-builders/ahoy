from flask import render_template
from app.config.extensions import db

#
#setup application wide error handlers
#
def register_error_handlers(app):
    #
    #install application wide 404 error handler
    @app.errorhandler(404)
    def not_found(e):
        #return render_template('404.html'), 404
        return app.send_static_file("html/404.html"), 404

    #
    #install application wide 500 error handler
    @app.errorhandler(500)
    def internal_server_error(e):
        #return render_template('500.html'), 500
        return app.send_static_file("html/500.html") , 500


    # @app.errorhandler(Exception)
    # def error(e):
    #     return "duplicate email error"




