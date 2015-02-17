import datetime

def register_jinja_filters(app):

    #copyright year filter
    @app.template_filter()
    def copyright_year(value):
        return datetime.datetime.utcnow().year

    #add copyright year filter to jinja template
    app.jinja_env.filters['copyright_year'] = copyright_year
