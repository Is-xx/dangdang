from django.urls import path
from cart import views

app_name = 'cart'

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('add_cart/', views.add_cart, name='add_cart'),
    path('sub_cart/', views.sub_cart, name='sub_cart'),
    path('total_book/', views.total_book, name='total_book'),
    path('del_cart/', views.del_cart, name='del_cart'),
    path('big_total/', views.big_total, name='big_total'),
    path('add_login_cart/', views.add_login_cart, name='add_login_cart'),
    path('sub_login_cart/', views.sub_login_cart, name='sub_login_cart'),
    path('total_login_book/', views.total_login_book, name='total_login_book'),
    path('del_login_cart/', views.del_login_cart, name='del_login_cart'),
]