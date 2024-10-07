from django.db import models
from django.contrib.auth.models import User


class Stock(models.Model):
    #im pretty sure all tickers are shorter than 10 chars
    ticker = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = 3)

    def __str__(self):
        return self.ticker
