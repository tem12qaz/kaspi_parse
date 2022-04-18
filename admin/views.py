from flask import redirect, url_for, request
from flask_security import current_user

from flask_admin import BaseView, AdminIndexView, expose

from flask_admin.contrib.sqla import ModelView


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class HomeAdminView(AdminMixin, AdminIndexView):
    @expose('/kaspi')
    def index(self):
        return self.render('admin_home.html')


class ProductView(AdminMixin, ModelView):
    # column_list = ('id', 'region', 'name', 'kaspi_price', 'kaspi_url', 'supplier1_code', 'supplier1_price', 'supplier1_margin')
    column_list = ('id', 'commission', 'kaspi_price', 'kaspi_url',
                   'supplier1', 'supplier2', 'supplier3', 'supplier4',
                   'supplier5', 'supplier6', 'supplier7', 'supplier8',
                   'supplier9', 'supplier10', 'best'
                   )

    form_columns = ('kaspi_url', 'supplier1_code', 'supplier1_code',
                    'supplier2_code', 'supplier3_code', 'supplier4_code',
                    'supplier5_code', 'supplier6_code', 'supplier7_code',
                    'supplier8_code', 'supplier9_code', 'supplier10_code',
                    'commission')


class CommView(AdminMixin, ModelView):
    column_list = ('id', 'commission', 'delivery_price', 'delivery_duration_from', 'delivery_duration_to')

    form_columns = tuple()


class ProxyView(AdminMixin, ModelView):
    column_list = ('id', 'user', 'password', 'ip', 'port', 'status')
    form_columns = ('user', 'password', 'ip', 'port', 'status')


class LogoutView(AdminMixin, BaseView):
    @expose('/kaspi')
    def logout_button(self):
        return redirect(url_for('security.logout', next='/admin'))
