from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView, TemplateView

from admins.forms import UserAdminRegisterForm, UserAdminProfileForm, CategoryUpdateFormAdmin, ProductsForm
from authapp.models import User
from mainapp.mixin import BaseClassContextMixin, CustomDispatchMixin
from mainapp.models import Product, ProductCategory

from django.utils.translation import gettext_lazy as _


class IndexTemplateView(TemplateView, CustomDispatchMixin):
    template_name = 'admins/admin.html'


# Users
class UserListView(ListView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-read.html'


class UserCreateView(CreateView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('admins:admin_users')


class UserUpdateView(UpdateView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')


class UserDeleteView(DeleteView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# Category
class CategoryListView(ListView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-read.html'

    def get_queryset(self):
        if self.kwargs:
            return ProductCategory.objects.filter(id=self.kwargs.get('pk'))
        else:
            return ProductCategory.objects.all()


class CategoryDeleteView(DeleteView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-update-delete.html'
    success_url = reverse_lazy('admins:admin_category')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = not self.object.is_active
        self.object.save()
        product_list = Product.objects.filter(category__pk=self.kwargs.get('pk'))
        for product in product_list:
            if product.is_active:
                product.is_active = not product.is_active
                product.save()
        return HttpResponseRedirect(self.get_success_url())


class CategoryUpdateView(UpdateView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-update-delete.html'
    form_class = CategoryUpdateFormAdmin
    success_url = reverse_lazy('admins:admin_category')


class CategoryCreateView(CreateView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-create.html'
    success_url = reverse_lazy('admins:admin_category')
    form_class = CategoryUpdateFormAdmin


# Product
class ProductListView(ListView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-product-read.html'


class ProductsUpdateView(UpdateView, BaseClassContextMixin, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-products-update-delete.html'
    form_class = ProductsForm
    title = 'Админка | Обновление продукта'
    success_url = reverse_lazy('admins:admins_product')


class ProductsCreateView(CreateView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-products-create.html'
    form_class = ProductsForm
    success_url = reverse_lazy('admins:admins_product')


class ProductsDeleteView(DeleteView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-product-read.html'
    success_url = reverse_lazy('admins:admins_product')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = not self.object.is_active
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
