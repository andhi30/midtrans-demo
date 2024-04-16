from django.contrib import admin

from .models import Coin, Product, Purchase, Website, CoinPurchase


@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ("user", "balance", "purchase_count")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "sold_count")
    ordering = ("id",)


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "created_at")


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ("owner", "created_at")

@admin.register(CoinPurchase)
class CoinPurchaseAdmin(admin.ModelAdmin):
    list_display = ("user", "transaction_token", "created_at")