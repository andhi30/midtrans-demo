from django.urls import path

from . import views

urlpatterns = [
    path("", views.wallet, name="wallet"),
    path("topup/payment", views.topup_payment, name="topup_payment"),
    path("topup/payment/success", views.topup_payment_success, name="topup_success"),
]