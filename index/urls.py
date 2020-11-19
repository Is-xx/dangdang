from django.urls import path
from index import views

app_name = 'index'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('detail/', views.detail, name='detail'),
    path('list/', views.list, name='list'),
    path('quit/', views.quit, name='quit'),
]