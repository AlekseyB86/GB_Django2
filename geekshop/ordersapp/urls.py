from django.urls import path

from ordersapp.views import OrderListView, OrderCreateView, OrderUpdateView, OrderDeleteView, OrderDetailView, \
    order_forming_complete
# from ordersapp.views import order_change_status

app_name = 'ordersapp'
urlpatterns = [

    path('', OrderListView.as_view(), name='list'),
    path('create/', OrderCreateView.as_view(), name='create'),
    path('update/<int:pk>/', OrderUpdateView.as_view(), name='update'),
    path('read/<int:pk>/', OrderDetailView.as_view(), name='read'),
    path('delete/<int:pk>/', OrderDeleteView.as_view(), name='delete'),
    path('forming_complete/<int:pk>/', order_forming_complete, name='forming_complete'),
    # path('change_status/<int:pk>/', order_change_status, name='change_status'),

]