from django.urls import path
from . import views

app_name = "HOS"

urlpatterns = [
    path("", views.index, name="index"),
    path("form/hos/", views.hos_form, name="form"),
    path("email/hos/", views.hos_report, name="email"),
    path("form/hos/confirmation", views.hos_form, name="form"),
]
