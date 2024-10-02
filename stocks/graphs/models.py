from django.db import models

class Stock(models.Model):
    #im pretty sure all tickers are shorter than 10 chars
    ticker = models.CharField(max_length=10)

    def __str__(self):
        return self.ticker
