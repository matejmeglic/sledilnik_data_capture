"""declaration"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('HOS_form/', views.HOS_form, name='HOS_form'),
]
