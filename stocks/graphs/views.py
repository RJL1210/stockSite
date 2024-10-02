from django.shortcuts import render
from django.conf import settings

def home(request):
    import requests
    import json

    context = {
        "api_key": settings.ALPHA_VANTAGE_API,
    }
    

    if request.method == 'POST':
        ticker = request.POST['Ticker']

        default_url = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo')
        daily_url = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=' + ticker +'&apikey=' + context['api_key'])

        overview_default = requests.get('https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo')
        overview_url = requests.get('https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo')
        #daily_url = 
        #daily_req = requests.get(daily_url)

        try:
            api = json.loads(daily_url.content)
            processed_api = {}
            if api['Information']:
                api = json.loads(default_url.content)
                overview = json.loads(overview_default.content)
                processed_api['outOfCalls'] = True
            else:    
                overview = json.loads(overview_url.content)
            processed_api['symbol'] = api['Global Quote']['01. symbol']
            processed_api['open'] = api['Global Quote']['02. open']
            processed_api['high'] = api['Global Quote']['03. high']
            processed_api['low'] = api['Global Quote']['04. low']
            processed_api['price'] = api['Global Quote']['05. price']
            processed_api['volume'] = api['Global Quote']['06. volume']
            processed_api['latest trading day'] = api['Global Quote']['07. latest trading day']
            processed_api['previous close'] = api['Global Quote']['08. previous close']
            processed_api['change'] = api['Global Quote']['09. change']
            processed_api['change percent'] = api['Global Quote']['10. change percent']

            processed_api['marketcap'] = overview['MarketCapitalization']
            processed_api['companyname'] = overview['Name']
            processed_api['52weekhigh'] = overview['52WeekHigh']
            processed_api['52weeklow'] = overview['52WeekLow']

        except Exception as e:
            api = "Error..."
            processed_api = {}
        return render(request, 'home.html', {'api': api, 'processed_api': processed_api})
    else:
        return render(request, 'home.html', {'Ticker': "Search for a stock ticker above"})

    

def about(request):
    return render(request, 'about.html', {})