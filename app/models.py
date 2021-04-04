from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class ScraperCategory(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    cat_id = db.Column(db.Integer)
    cat_link = db.Column(db.String(512))
    cat_name = db.Column(db.String(512))
    shop = db.Column(db.String(128))

    def __repr__(self):
        return "<Category {}>".format(self.cat_link)


class PlasticServices(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    service = db.Column(db.String(512))
    description = db.Column(db.String(1512))
    service_id = db.Column(db.Integer)
    host_service_name = db.Column(db.String(512))

    def __repr__(self):
        return "<Service {}>".format(self.service)


class BeautyServices(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    service = db.Column(db.String(512))
    description = db.Column(db.String(1512))
    service_id = db.Column(db.Integer)
    host_service_name = db.Column(db.String(512))

    def __repr__(self):
        return "<Service {}>".format(self.service)