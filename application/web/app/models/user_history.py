from flask import current_app
from app.config.extensions import db, bcrypt,flaskuuid,login_manager
from flask.ext.login import make_secure_token, current_user
from datetime import datetime
import uuid
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import \
    ARRAY, BIGINT, BIT, BOOLEAN, BYTEA, CHAR, CIDR, DATE, \
    DOUBLE_PRECISION, ENUM, FLOAT, HSTORE, INET, INTEGER, \
    INTERVAL, JSON, JSONB, MACADDR, NUMERIC, OID, REAL, SMALLINT, TEXT, \
    TIME, TIMESTAMP, UUID, VARCHAR, INT4RANGE, INT8RANGE, NUMRANGE, \
    DATERANGE, TSRANGE, TSTZRANGE, TSVECTOR


class UserHistory(db.Model):
    __tablename__ = "user_history"
    #uid = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,nullable=False, index=True)
    user_uuid = Column(UUID(as_uuid=True),nullable=False, default=uuid.uuid4)
    #user_uuid = Column(UUID, nullable=False,default=uuid.uuid4)
    username = db.Column(db.String(255),nullable=False, index=True)
    email = db.Column(db.String(255),nullable=False, unique=True, index=True)
    action = db.Column(db.String(255),nullable=False, index=True)
    created_at = db.Column(db.DateTime,nullable=False, index=True,default=datetime.utcnow)
