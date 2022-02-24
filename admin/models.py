from flask_security import UserMixin, RoleMixin

from flask_app_init import db

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                       )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))


class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    region = db.Column(db.String(128), nullable=True)
    name = db.Column(db.String(512), nullable=True)
    kaspi_price = db.Column(db.Integer(), nullable=True)
    kaspi_url = db.Column(db.Integer())
    supplier1_code = db.Column(db.String(128))
    supplier1_name = db.Column(db.String(128), nullable=True)
    supplier1_price = db.Column(db.Integer(), nullable=True)
    supplier1_margin = db.Column(db.Integer(), nullable=True)
    supplier1_margin_percent = db.Column(db.Float(), nullable=True)


class Commission(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    commission = db.Column(db.Integer())
    delivery_price = db.Column(db.Integer())


