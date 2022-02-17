from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

import os

from django.views.generic import DetailView
from django.conf import settings
from django.core.cache import cache

from mainapp.models import Product, ProductCategory

MODULE_DIR = os.path.dirname(__file__)


# Create your views here.

def index(request):
    context = {
        'title': 'Geekshop', }
    return render(request, 'mainapp/index.html', context)


def get_link_category():
    if not settings.LOW_CACHE:
        return ProductCategory.objects.all()
    key = 'link_category'
    link_category = cache.get(key)
    if link_category is None:
        link_category = ProductCategory.objects.all()
        cache.set(key, link_category)
    return link_category


def get_product():
    if not settings.LOW_CACHE:
        return Product.objects.all().select_related('category')
    key = 'link_product'
    link_product = cache.get(key)
    if link_product is None:
        link_product = Product.objects.all().select_related('category')
        cache.set(key, link_product)
    return link_product


def get_product_one(pk):
    if not settings.LOW_CACHE:
        return Product.objects.get(id=pk)
    key = f'product{pk}'
    product = cache.get(key)
    if product is None:
        product = Product.objects.get(id=pk)
        cache.set(key, product)
    return product


def products(request, id_category=None, page=1):
    if id_category:
        products = Product.objects.filter(category_id=id_category).select_related('category')
    else:
        products = Product.objects.all().select_related()
    products = get_product()
    paginator = Paginator(products, per_page=3)

    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': 'Geekshop | Каталог',
        'products': products_paginator,
        # 'categories': ProductCategory.objects.all(),
        'categories': get_link_category(),
    }

    return render(request, 'mainapp/products.html', context)


class ProductDetail(DetailView):
    """
    Контроллер вывода информации о продукте
    """
    model = Product
    template_name = 'mainapp/detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        # product = self.get_object()
        context['product'] = get_product_one(self.kwargs.get('pk'))
        return context
