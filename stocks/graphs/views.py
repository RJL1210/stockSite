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
    except Exception as e:
        api = "Error..."


    return render(request, 'home.html', {'api': api,})

def about(request):
    return render(request, 'about.html', {})