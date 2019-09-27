from project import db, bcrypt
from sqlalchemy.sql import func
import json


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    images = db.relationship('Image', backref='user', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode()

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at
        }


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    is_private = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    boxes = db.relationship('Box', backref='image', lazy='dynamic')

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'uploaded_at': self.uploaded_at
        }


class Box(db.Model):
    __tablename__ = 'boxes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(64), nullable=False)
    x_min = db.Column(db.Float, nullable=False)
    y_min = db.Column(db.Float, nullable=False)
    x_max = db.Column(db.Float, nullable=False)
    y_max = db.Column(db.Float, nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'))

    def to_json(self):
        return {
            'label': self.label,
            'x_min': self.x_min,
            'y_min': self.y_min,
            'x_max': self.x_max,
            'y_max': self.y_max
        }
