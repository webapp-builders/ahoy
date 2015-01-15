def register_blueprints(app):
    from app.responders.home import home
    app.register_blueprint(home)

    from app.responders.account import account
    app.register_blueprint(account)
