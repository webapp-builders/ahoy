from flask import current_app
from app.config.extensions import db, bcrypt,flaskuuid,login_manager
from flask.ext.login import make_secure_token, current_user
from datetime import datetime,timedelta
import uuid,json
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import \
    ARRAY, BIGINT, BIT, BOOLEAN, BYTEA, CHAR, CIDR, DATE, \
    DOUBLE_PRECISION, ENUM, FLOAT, HSTORE, INET, INTEGER, \
    INTERVAL, JSON, JSONB, MACADDR, NUMERIC, OID, REAL, SMALLINT, TEXT, \
    TIME, TIMESTAMP, UUID, VARCHAR, INT4RANGE, INT8RANGE, NUMRANGE, \
    DATERANGE, TSRANGE, TSTZRANGE, TSVECTOR
from werkzeug.security import generate_password_hash, check_password_hash
#from sqlalchemy_utils import UUIDType
#flask.ext.sqlalchemy.get_debug_queries()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    uuid = Column(UUID(as_uuid=True),nullable=False, default=uuid.uuid4)
    username = db.Column(db.String(255),nullable=False, index=True)
    email = db.Column(db.String(255),nullable=False, unique=True, index=True)
    password = db.Column(db.String(2048),nullable=False)
    signin_token = db.Column(db.String(2048),nullable=True, unique=True, index=True)
    verified = db.Column(db.Boolean,nullable=False,default=False)
    verified_at = db.Column(db.DateTime,nullable=True)
    verification_token = db.Column(db.String(2048),nullable=True, unique=True, index=True)
    verification_token_expires_at = db.Column(db.DateTime,nullable=True)
    banned = db.Column(db.Boolean,nullable=False,default=False)
    ban_reason=db.Column(db.String(2048),nullable=True)
    created_at = db.Column(db.DateTime,nullable=False, index=True,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    lastvisit_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    lastsignin_at = db.Column(db.DateTime,nullable=True)
    lastsignout_at = db.Column(db.DateTime,nullable=True)
    role = db.Column(db.String(50),nullable=False,default="member") #options: "member" or "mod" or "admin" or "sa"
    password_reset_token = db.Column(db.String(2048),nullable=True, unique=True, index=True)
    password_reset_token_expires_at = db.Column(db.DateTime,nullable=True)
    lockedout = db.Column(db.Boolean,nullable=False,default=False)
    lockout_expires_at = db.Column(db.DateTime,nullable=True)
    invalid_password_attempts=db.Column(db.Integer,nullable=False,default=0)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email.strip()).first()

    @staticmethod
    def get_by_signin_token(token):
        return User.query.filter_by(signin_token=token).first()

    @staticmethod
    def signup(form):
        email = form.email.data.strip()
        username=form.username.data.strip()
        token = make_secure_token(uuid.uuid4().hex)
        user = User(username=username,
                    email=email,
                    password=bcrypt.generate_password_hash(form.password.data.strip()),
                    verification_token=token,
                    verification_token_expires_at=datetime.utcnow() + timedelta(days=1))
        db.session.add(user)
        db.session.commit()
        return username,email,token

    @staticmethod
    def validate(email):
        email = email.strip()
        user = User.query.filter_by(email=email).first()
        if user and not user.verified:
            token = make_secure_token(uuid.uuid4().hex)
            user.verification_token=token,
            user.verification_token_expires_at=datetime.utcnow() + timedelta(days=1)
            db.session.commit()
        return user


    @staticmethod
    def refresh_password_reset_token(email):
        email = email.strip()
        user = User.query.filter_by(email=email).first()
        if user and not user.banned:
            token = make_secure_token(uuid.uuid4().hex)
            user.password_reset_token=token,
            user.password_reset_token_expires_at=datetime.utcnow() + timedelta(minutes=15)
            db.session.commit()
        return user


    @staticmethod
    def signin(form):
        user = User.query.filter_by(email=form.email.data.strip()).first()
        if user:
            user.authenticated = False;
            if user.verified and not user.banned:
                user.unlock_if_lockedout_and_lockout_period_expired()
                if not user.lockedout:
                    if bcrypt.check_password_hash(user.password, form.password.data.strip()):
                        user.authenticate()
                    else:
                        user.invalid_password_attempts = user.invalid_password_attempts + 1
                        user.lockout_max_password_attempts()
                    db.session.commit()
        return user


    @staticmethod
    def account_verified(request):
        token = request.args.get('token')
        if token:
            email = request.args.get('email')
            if email:
                user = User.query.filter_by(email=email).first()
                if user:
                    user.authenticated = False
                    if not user.verified:
                        if user.verification_token == token.strip():
                            if datetime.utcnow() < user.verification_token_expires_at:
                                user.verify_and_authenticate()
                        #we only check one time if token matches then clear it regardless
                        user.verification_token = None
                        user.verification_token_expires_at = datetime.utcnow()
                        db.session.commit()
        return user


    """
    this method will unlock a lockedout account since we have a 15 minute expiring token
    and we are changing the password anyway this method will also verify the user account
    """
    @staticmethod
    def reset_password(form,request):
        token = request.args.get('token')
        if token:
            user = User.query.filter_by(email=form.email.data.strip()).first()
            if user:
                user.password_reset_token
                user.authenticated = False
                if user.password_reset_token == token.strip():
                    if datetime.utcnow() < user.password_reset_token_expires_at:
                        user.verify_and_authenticate()
                        user.password = bcrypt.generate_password_hash(form.password.data.strip())
                #we only check one time if token matches then clear it regardless
                user.password_reset_token = None
                user.password_reset_token_expires_at = datetime.utcnow()
                db.session.commit()
        return user



    def unlock_if_lockedout_for_password_reset(self):
        if self.lockedout:
            #if bool(current_app.config["PASSWORD_RESET_LOCKOUT_UNLOCK_POLICY"]):
            self.invalid_password_attempts=0
            serf.lockout_expires_at=None
            self.lockedout=False

    def unlock_if_lockedout_and_lockout_period_expired(self):
        if self.lockedout:
            #if bool(current_app.config["EXPIRED_LOCKOUT_UNLOCK_POLICY"]):
            if self.lockout_expires_at < datetime.utcnow:
                self.invalid_password_attempts=0
                serf.lockout_expires_at=None
                self.lockedout=False



    def verify_and_authenticate(self):
        now = datetime.utcnow()
        self.verified=True
        self.verified_at = now
        self.signin_token = make_secure_token(uuid.uuid4().hex)
        self.authenticated=True
        self.lastsignin_at = now
        self.updated_at =  now


    def authenticate(self):
        now = datetime.utcnow()
        self.signin_token = make_secure_token(uuid.uuid4().hex)
        self.authenticated=True
        self.lastsignin_at = now
        self.updated_at =  now

    def lockout_max_password_attempts(self):
        now = datetime.utcnow()
        minutes = int(current_app.config["SIGNIN_LOCKOUT_DURATION"])
        if self.invalid_password_attempts == current_app.config["MAX_INVALID_PASSWORD_ATTEMPTS"]:
            self.lockout_expires_at = now + timedelta(minutes=minutes)
            self.lockedout = True



    # flask login methods
    def is_authenticated(self):
        return self.authenticated and not self.banned

    def is_anonymous(self):
        return False;

    def is_active(self):
        return self.authenticated and self.verified and not self.banned and not self.lockedout

    def get_id(self):
        return unicode(self.signin_token)
    # end flask login methods



    # flask login accesses this method which causes a sql query
    # def __repr__(self):
    #     return '<User %r >' % self.username


#required flask login function for user token based authentication
#flask login calls the get_id method of User model in the login_user(user) method
#to get a user id token
#then passes the token to load_user function as the user_id parameter
def load_user(user_id):
    user = User.get_by_signin_token(user_id)
    if user:
        user.authenticated = True
        user.lastvisit_at = datetime.utcnow()
        db.session.commit()
    return user




