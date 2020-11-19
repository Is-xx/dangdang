from django.urls import path
from indent import views

app_name = 'indent'

urlpatterns = [
    path('indent/', views.indent, name='indent'),
    path('indent_ok/', views.indent_ok, name='indent_ok'),
    path('exit/', views.exit, name='exit'),
    path('indent_submit/', views.indent_submit, name='indent_submit'),
    path('select/', views.select, name='select'),
]