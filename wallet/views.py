import secrets

import midtransclient
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from midtransclient import CoreApi, Snap

from .models import CoinPurchase, Product

MIDTRANS_CLIENT: CoreApi = midtransclient.CoreApi(
    is_production=not settings.DEBUG,
    server_key=settings.MIDTRANS_SERVER_KEY,
    client_key=settings.MIDTRANS_CLIENT_KEY,
)

MIDTRANS_SNAP: Snap = midtransclient.Snap(
    is_production=not settings.DEBUG,
    server_key=settings.MIDTRANS_SERVER_KEY,
    client_key=settings.MIDTRANS_CLIENT_KEY,
)

PRICING_PLANS = [
    {
        "id": 1,
        "name": "Starter Plan",
        "price": 10_000,
        "coin": 100,
    },
    {
        "id": 2,
        "name": "Pro Plan",
        "price": 50_000,
        "coin": 500,
    },
    {
        "id": 3,
        "name": "Premium Plan",
        "price": 90_000,
        "coin": 1000,
    },
]

USER = User.objects.get(username="andhi")


def generate_transaction_token():
    return secrets.token_urlsafe(32)


def wallet(request):
    products = Product.objects.all()
    context = {
        "products": products,
        "user": USER,
        "pricing_plans": PRICING_PLANS,
        "client_key": settings.MIDTRANS_CLIENT_KEY,
    }
    return render(request, "wallet.html", context)


def topup_payment(request):
    if request.method == "POST":
        param = {
            "transaction_details": {
                "order_id": request.POST.get("order_id"),
                "gross_amount": request.POST.get("amount"),
            },
        }

        transaction = MIDTRANS_SNAP.create_transaction(param)

        transaction_token = transaction.get("token")
        transaction_redirect_url = transaction.get("redirect_url")

        CoinPurchase.objects.create(
            user=USER,
            transaction_token=transaction_token,
        ).save()

        return JsonResponse(
            {"token": transaction_token, "redirect_url": transaction_redirect_url}
        )
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


def topup_payment_success(request):
    if request.method == "POST":
        token = request.POST.get("token")

        get_object_or_404(CoinPurchase, transaction_token=token).delete()

        order_id = request.POST.get("order_id")
        # {date}-{time}-{order}-{order_id}

        order_id = order_id.split("-")[1]
        print(f"order_id: {order_id}")

        coin = PRICING_PLANS[int(order_id) - 1]["coin"]
        print(f"coin: {coin}")

        USER.coin.balance += coin
        USER.coin.save()

        return JsonResponse(
            {"balance": USER.coin.balance, "message": "Balance updated successfully"},
            status=200,
        )
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)
