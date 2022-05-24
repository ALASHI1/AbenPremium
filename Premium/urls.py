from django.urls import path
from Premium import views

urlpatterns = [
    path("cancelsub/", views.cancel_subscription, name="cancelsub"),
    path("subcribe", views.resub, name="subcribe"),
]
