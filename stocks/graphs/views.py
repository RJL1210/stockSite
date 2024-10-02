from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .models import Stock
from .forms import StockForm

def home(request):
    import requests
    import json

    context = {
        "api_key": settings.ALPHA_VANTAGE_API,
    }
    

    if request.method == 'POST':
        ticker = request.POST['ticker']

        default_url = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo')
        daily_url = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=' + ticker +'&apikey=' + context['api_key'])

        overview_default = requests.get('https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo')
        overview_url = requests.get('https://www.alphavantage.co/query?function=OVERVIEW&symbol=' + ticker + '&apikey=' + context['api_key'])

        try:
            api = json.loads(daily_url.content)
            processed_api = {}
            # Check if the API call was successful
            try:
                if api['Global Quote']:
                    # API call was successful
                    overview = json.loads(overview_url.content)
                    processed_api['outOfCalls'] = False
            except Exception as e:
                #out of calls
                api = json.loads(default_url.content)
                overview = json.loads(overview_default.content)
                processed_api['outOfCalls'] = True


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
            #invalid ticker
            api = "Error..."
            processed_api = {}
        return render(request, 'home.html', {'api': api, 'processed_api': processed_api})
    else:
        #default display
        return render(request, 'home.html', {'Ticker': "Search for a stock ticker above"})

    

def about(request):
    return render(request, 'about.html', {})

def add_stock(request):

    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ('Stock has been added'))
            return redirect('add_stock')
    else:

    
        ticker = Stock.objects.all()

        return render(request, 'add_stock.html', {'ticker': ticker})
    
def delete_stock(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()

    messages.success(request, ('Stock has been deleted'))

    return redirect(add_stock)