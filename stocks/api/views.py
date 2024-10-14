from django.shortcuts import render
from rest_framework import viewsets
from .serializers import StockSerializer
from .models import Stock

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
