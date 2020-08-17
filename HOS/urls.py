from django.urls import path
from . import views

app_name = "HOS"

urlpatterns = [
    path("", views.index, name="index"),
    path("form/hos/", views.hos_form, name="form"),
    path("report/hos/<int:report_id>/", views.hos_report, name="report"),
    path("form/hos/confirmation/", views.hos_form, name="form"),
]
