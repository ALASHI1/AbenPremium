from django.contrib.auth.views import LoginView
from django.urls import path

from Account import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("table", views.table, name="table"),
    path(
        "accounts/register/",
        views.MyRegistrationView.as_view(),
        name="django_registration_register",
    ),
    path(
        "accounts/activate/complete/",
        LoginView.as_view(),
        name="logins",
    ),
]
