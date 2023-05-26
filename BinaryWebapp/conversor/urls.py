
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('decimal/', views.decimal_views, name="decimal"),
    path('octal/', views.octal_views, name='octal'),
    path('hexadecimal/', views.hex_view, name='hexadecimal'),
    path('binary/', views.binary_view, name='binary'),
]
