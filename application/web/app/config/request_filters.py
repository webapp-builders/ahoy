from flask import g,request

class Visitor():
    def __init__(self,user):
        self.id=user.id
        self.name=user.username
        self.email=user.email

#
#setup per http request filters
#note: the g variable is a per request thread global
#
def register_per_request_filters(app):
    @app.before_request
    def app_before_request():
        # token=request.cookies.get("ahoy")
        # user = User.get_by_signin_token(token)
        # visitor = Visitor(user)
        #g.user=user
        pass

    @app.teardown_request
    def app_teardown_request(exception):
        user = getattr(g, 'current_user', None)
        if user is not None:
            print user

    @app.after_request
    def app_after_req(response):
        user = getattr(g, 'current_user', None)
        if user is not None:
            print g.current_user
        return response
