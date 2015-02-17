def register_blueprints(app):
    from app.responders.home import home
    app.register_blueprint(home)

    from app.responders.account import account
    app.register_blueprint(account)

    from app.responders.event import event
    app.register_blueprint(event)

    from app.responders.demo import demo
    app.register_blueprint(demo)

    #API Blueprints
    from app.api.v1.event import event as event_v1
    app.register_blueprint(event_v1,url_prefix='/api/v1')
