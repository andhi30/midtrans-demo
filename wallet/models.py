from django.db import models
from django.utils import timezone


class Coin(models.Model):
    user = models.OneToOneField(
        "auth.User", on_delete=models.CASCADE, related_name="coin"
    )
    balance = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} Coin"

    @property
    def purchase_count(self):
        return Purchase.objects.filter(user=self.user).count()


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.price}c"

    @property
    def sold_count(self):
        return Purchase.objects.filter(product=self).count()


class Purchase(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)


class CoinPurchase(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    transaction_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)


class Website(models.Model):
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    html = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.owner.username} Website"
