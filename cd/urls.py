from django.urls import path

from . import views

urlpatterns = [
    path("plans/", views.tariffs, name="plans"),
    path("new_contact/", views.ContactView.as_view(), name="new_contact"),
    path("cd_exchange/", views.exchange, name="cd_exchange"),
    path("thank-you/", views.thank_you),
]
