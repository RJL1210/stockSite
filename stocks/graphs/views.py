from django.shortcuts import render
from django.conf import settings

def home(request):
    import requests
    import json

    context = {
        "api_key": settings.ALPHA_VANTAGE_API,
    }
    
    
    url = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo')

    try:
        api = json.loads(url.content)
        processed_data = { 
            'symbol': api['Global Quote']['01. symbol'],
            'open': api['Global Quote']['02. open'],
            'high': api['Global Quote']['03. high'],
            'low': api['Global Quote']['04. low'],
            'price': api['Global Quote']['05. price'],
            'volume': api['Global Quote']['06. volume'],
            'latest trading day': api['Global Quote']['07. latest trading day'],
            'previous close': api['Global Quote']['08. previous close'],
            'change': api['Global Quote']['09. change'],
            'change percent': api['Global Quote']['10. change percent'],
        }
    except Exception as e:
        api = "Error..."


    return render(request, 'home.html', {'api': api, 'processed_api': processed_data})

def about(request):
    return render(request, 'about.html', {})