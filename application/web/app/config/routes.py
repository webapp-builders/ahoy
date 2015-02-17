#optionally use this function to add  application routing rules in a single location
#all the application routes can be specified here instead of using attribute routing
#or you can use a combination of both specifying only some of the route rules in this function
def add_url_rules(app):
    pass
    #sample routs:
    #view_func is the actual view function prefixed by the imported module name (i.e. file name)
    #endpoint can be any unique name per bluepring. Generally the view function name is used.
    #Note: print app.url_map will display mapping rules as blueprintname.endpointname not as the view_func value

    # from app.responders import home
    # home.home.add_url_rule('/', endpoint='index',view_func=home.index)

    # from app.responders import account
    # account.account.add_url_rule('/account/signup', endpoint='signup',view_func=account.signup)

    #from app.responders import event
    #event.event.add_url_rule('/events/<id>', endpoint='upsert',view_func=event.upsert, defaults={'id': None}, methods=['GET','POST'])



