import os

class Settings:
    def __init__(self):
        self.SECRET_KEY = os.environ.get('SECRET_KEY')#os.urandom(24)
        self.DEBUG = bool(os.environ.get('DEBUG'))
        self.SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
        #Note:SQLALCHEMY_COMMIT_ON_TEARDOWN = True sets response headers in the
        #stream prior to app.errorhandler(Exception)
        #self.SQLALCHEMY_COMMIT_ON_TEARDOWN = True
        self.SQLALCHEMY_RECORD_QUERIES = True #records queries
        self.SQLALCHEMY_ECHO = True #logs queries
        self.DEBUG_TB_INTERCEPT_REDIRECTS = False
        self.ITEMS_PER_PAGE = int(os.environ.get('ITEMS_PER_PAGE'))
        self.SIGNIN_LOCKOUT_DURATION=int(os.environ.get('SIGNIN_LOCKOUT_DURATION'))
        self.MAX_INVALID_PASSWORD_ATTEMPTS=int(os.environ.get('MAX_INVALID_PASSWORD_ATTEMPTS'))
        self.EXPIRED_LOCKOUT_UNLOCK_POLICY=bool(os.environ.get('EXPIRED_LOCKOUT_UNLOCK_POLICY'))
        self.SIGNIN_LOCKOUT_ENABLED=bool(os.environ.get('SIGNIN_LOCKOUT_ENABLED'))
