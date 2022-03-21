import enum

from flask_security import UserMixin, RoleMixin
from jinja2 import Markup
from tabulate import tabulate

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


class Proxy(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user = db.Column(db.String(32))
    password = db.Column(db.String(32))
    ip = db.Column(db.String(32))
    port = db.Column(db.String(32))
    status = db.Column(db.String(16), default='OK')

    def __repr__(self):
        return f'http://{self.user}:{self.password}@{self.ip}:{self.port}/'


class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    region = db.Column(db.String(128), nullable=True)
    name = db.Column(db.String(512), nullable=True)
    kaspi_price = db.Column(db.Integer(), nullable=True)
    kaspi_url = db.Column(db.String(512))

    supplier1_code = db.Column(db.String(128), nullable=True)
    supplier1_amount = db.Column(db.String(128), nullable=True)
    supplier1_name = db.Column(db.String(128), nullable=True)
    supplier1_price = db.Column(db.Float(), nullable=True)
    supplier1_margin = db.Column(db.Float(), nullable=True)
    supplier1_margin_percent = db.Column(db.Float(), nullable=True)

    supplier2_code = db.Column(db.String(128), nullable=True)
    supplier2_amount = db.Column(db.String(128), nullable=True)
    supplier2_name = db.Column(db.String(128), nullable=True)
    supplier2_price = db.Column(db.Float(), nullable=True)
    supplier2_margin = db.Column(db.Float(), nullable=True)
    supplier2_margin_percent = db.Column(db.Float(), nullable=True)

    supplier3_code = db.Column(db.String(128), nullable=True)
    supplier3_amount = db.Column(db.String(128), nullable=True)
    supplier3_name = db.Column(db.String(128), nullable=True)
    supplier3_price = db.Column(db.Float(), nullable=True)
    supplier3_margin = db.Column(db.Float(), nullable=True)
    supplier3_margin_percent = db.Column(db.Float(), nullable=True)

    supplier4_code = db.Column(db.String(128), nullable=True)
    supplier4_amount = db.Column(db.String(128), nullable=True)
    supplier4_name = db.Column(db.String(128), nullable=True)
    supplier4_price = db.Column(db.Float(), nullable=True)
    supplier4_margin = db.Column(db.Float(), nullable=True)
    supplier4_margin_percent = db.Column(db.Float(), nullable=True)

    supplier5_code = db.Column(db.String(128), nullable=True)
    supplier5_amount = db.Column(db.String(128), nullable=True)
    supplier5_name = db.Column(db.String(128), nullable=True)
    supplier5_price = db.Column(db.Float(), nullable=True)
    supplier5_margin = db.Column(db.Float(), nullable=True)
    supplier5_margin_percent = db.Column(db.Float(), nullable=True)

    supplier6_code = db.Column(db.String(128), nullable=True)
    supplier6_amount = db.Column(db.String(128), nullable=True)
    supplier6_name = db.Column(db.String(128), nullable=True)
    supplier6_price = db.Column(db.Float(), nullable=True)
    supplier6_margin = db.Column(db.Float(), nullable=True)
    supplier6_margin_percent = db.Column(db.Float(), nullable=True)

    supplier7_code = db.Column(db.String(128), nullable=True)
    supplier7_amount = db.Column(db.String(128), nullable=True)
    supplier7_name = db.Column(db.String(128), nullable=True)
    supplier7_price = db.Column(db.Float(), nullable=True)
    supplier7_margin = db.Column(db.Float(), nullable=True)
    supplier7_margin_percent = db.Column(db.Float(), nullable=True)

    supplier8_code = db.Column(db.String(128), nullable=True)
    supplier8_amount = db.Column(db.String(128), nullable=True)
    supplier8_name = db.Column(db.String(128), nullable=True)
    supplier8_price = db.Column(db.Float(), nullable=True)
    supplier8_margin = db.Column(db.Float(), nullable=True)
    supplier8_margin_percent = db.Column(db.Float(), nullable=True)

    supplier9_code = db.Column(db.String(128), nullable=True)
    supplier9_amount = db.Column(db.String(128), nullable=True)
    supplier9_name = db.Column(db.String(128), nullable=True)
    supplier9_price = db.Column(db.Float(), nullable=True)
    supplier9_margin = db.Column(db.Float(), nullable=True)
    supplier9_margin_percent = db.Column(db.Float(), nullable=True)

    supplier10_code = db.Column(db.String(128), nullable=True)
    supplier10_amount = db.Column(db.String(128), nullable=True)
    supplier10_name = db.Column(db.String(128), nullable=True)
    supplier10_price = db.Column(db.Float(), nullable=True)
    supplier10_margin = db.Column(db.Float(), nullable=True)
    supplier10_margin_percent = db.Column(db.Float(), nullable=True)

    commission_id = db.Column(db.Integer, db.ForeignKey('commission.id'), nullable=False)

    def best_margin(self):
        margins = [getattr(self, f'supplier{i}_margin') for i in range(1, 11) if
                   getattr(self, f'supplier{i}_margin') is not None]
        if not margins:
            return 'Null', 'Null'
        best_margin = max(margins)

        supplier_margin = getattr(self, f'supplier{margins.index(best_margin) + 1}_name')

        return max(margins), supplier_margin

    def best_percent(self):
        margins_percent = [getattr(self, f'supplier{i}_margin_percent') for i in range(1, 11) if
                           getattr(self, f'supplier{i}_margin_percent') is not None]
        if not margins_percent:
            return 'Null', 'Null'
        best_margin_percent = max(margins_percent)

        supplier_margin_percent = getattr(self, f'supplier{margins_percent.index(best_margin_percent) + 1}_name')

        return max(margins_percent), supplier_margin_percent

    @property
    def best(self):
        margins = [getattr(self, f'supplier{i}_margin') for i in range(1, 11) if
                   getattr(self, f'supplier{i}_margin') is not None]
        margins_percent = [getattr(self, f'supplier{i}_margin_percent') for i in range(1, 11) if
                           getattr(self, f'supplier{i}_margin_percent') is not None]

        best_margin, supplier_margin = self.best_margin()
        best_margin_percent, supplier_margin_percent = self.best_percent()

        table = f'best_margin {best_margin} <b>{supplier_margin}</b><br>best_margin_percent {best_margin_percent} <b>{supplier_margin_percent}</b>'

        represent = Markup(
            f'<div style="max-width: 300px; white-space: pre">{table}</div>'.replace(' ', '&nbsp'))
        return represent

    def get_supplier_repr(self, num):
        name = getattr(self, f'supplier{num}_name')
        code = getattr(self, f'supplier{num}_code')
        amount = getattr(self, f'supplier{num}_amount')
        price = getattr(self, f'supplier{num}_price')
        margin = getattr(self, f'supplier{num}_margin')
        margin_percent = getattr(self, f'supplier{num}_margin_percent')

        if margin and margin == self.best_margin()[0]:
            margin = f'<font color="green">{margin}</font>'

        if margin_percent and margin_percent == self.best_percent()[0]:
            margin_percent = f'<font color="green">{margin_percent}</font>'

        if not name and not code:
            return 'null'

        table = f'<i>amount:</i> <b>{amount}</b><br><i>price:</i> <b>{price}</b><br><i>margin:</i> <b>{margin}</b><br><i>percent:</i> <b>{margin_percent}</b>'

        represent = Markup(
            f'<div style="max-width: 300px; white-space: pre"><b>{name}</b><br>{code}<br>{table}</div>'
                .replace(' ', '&nbsp').replace('<font&nbspcolor="green">', '<font color="green">'))
        return represent

    @property
    def supplier1(self):
        return self.get_supplier_repr(1)

    @property
    def supplier2(self):
        return self.get_supplier_repr(2)

    @property
    def supplier3(self):
        return self.get_supplier_repr(3)

    @property
    def supplier4(self):
        return self.get_supplier_repr(4)

    @property
    def supplier5(self):
        return self.get_supplier_repr(5)

    @property
    def supplier6(self):
        return self.get_supplier_repr(6)

    @property
    def supplier7(self):
        return self.get_supplier_repr(7)

    @property
    def supplier8(self):
        return self.get_supplier_repr(8)

    @property
    def supplier9(self):
        return self.get_supplier_repr(9)

    @property
    def supplier10(self):
        return self.get_supplier_repr(10)

    def __repr__(self):
        return f'''
kp = {self.kaspi_price}
s_name = {self.supplier1_name}
s_price = {self.supplier1_price}
s_margin = {self.supplier1_margin}
s_margin_percent = {self.supplier1_margin_percent}
'''


class Commission(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    commission = db.Column(db.Integer())
    delivery_price = db.Column(db.Integer())
    delivery_duration_from = db.Column(db.Integer())
    delivery_duration_to = db.Column(db.Integer())
    products = db.relationship('Product', backref='commission', lazy=True)
