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
    @expose('/')
    def index(self):
        return self.render('admin_home.html')


class ProductView(AdminMixin, ModelView):
    # column_list = ('id', 'region', 'name', 'kaspi_price', 'kaspi_url', 'supplier1_code', 'supplier1_price', 'supplier1_margin')
    column_list = ('id', 'kaspi_price', 'kaspi_url', 'supplier1_code', 'supplier1_price', 'supplier1_margin')

    form_columns = ('kaspi_url', 'supplier1_code')


class CommView(AdminMixin, ModelView):
    column_list = ('id', 'commission', 'delivery_price')

    form_columns = tuple()


class LogoutView(AdminMixin, BaseView):
    @expose('/')
    def logout_button(self):
        return redirect(url_for('security.logout', next='/admin'))
