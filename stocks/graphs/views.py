from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .models import Stock
from .forms import StockForm

context = {
        "api_key": settings.ALPHA_VANTAGE_API,
}

def readNumber(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        pass    

    if value >= 1_000_000_000_000:
        return f'{value / 1_000_000_000_000:.2f}T'
    elif value >= 1_000_000_000:
        return f'{value / 1_000_000_000:.2f}B'
    elif value >= 1_000_000:
        return f'{value / 1_000_000:.2f}M'
    elif value >= 1_000:
        return f'{value / 1_000:.2f}K'
    else:
        return str(value)

def home(request):
    import requests
    import json

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

            processed_api['marketcap'] = readNumber(overview['MarketCapitalization'])
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
        return render(request, 'home.html', {'Ticker': ""})

    

def about(request):
    return render(request, 'about.html', {})

def add_stock(request):
    import requests
    import json

    if request.method == 'POST':
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ('Stock has been added'))
            return redirect('add_stock')
    else:
        processed_apis = {}
        ticker = Stock.objects.all()

        for index, symb in enumerate(ticker):
            api_request = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + str(symb) + '&apikey=' + context['api_key'])
            overview_url = requests.get('https://www.alphavantage.co/query?function=OVERVIEW&symbol=' + str(symb) + '&apikey=' + context['api_key'])

            try: 
                api = json.loads(api_request.content)
                overview = json.loads(overview_url.content)
                curr_api = {}
                if 'Global Quote' in api:
                    curr_api['outOfCalls'] = False
                else:
                    raise KeyError
            except Exception as e:
                default_url = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo')
                overview_default = requests.get('https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo')
                api = json.loads(default_url.content)
                overview = json.loads(overview_default.content)
                curr_api = {}
                curr_api['outOfCalls'] = True

            curr_api['symbol'] = api['Global Quote'].get('01. symbol', 'N/A')
            curr_api['open'] = api['Global Quote'].get('02. open', 'N/A')
            curr_api['high'] = api['Global Quote'].get('03. high', 'N/A')
            curr_api['low'] = api['Global Quote'].get('04. low', 'N/A')
            curr_api['price'] = api['Global Quote'].get('05. price', 'N/A')
            curr_api['volume'] = api['Global Quote'].get('06. volume', 'N/A')
            curr_api['latest trading day'] = api['Global Quote'].get('07. latest trading day', 'N/A')
            curr_api['previous close'] = api['Global Quote'].get('08. previous close', 'N/A')
            curr_api['change'] = api['Global Quote'].get('09. change', 'N/A')
            curr_api['change percent'] = api['Global Quote'].get('10. change percent', 'N/A')

            curr_api['marketcap'] = readNumber(overview.get('MarketCapitalization', 'N/A'))
            curr_api['companyname'] = overview.get('Name', 'N/A')
            curr_api['52weekhigh'] = overview.get('52WeekHigh', 'N/A')
            curr_api['52weeklow'] = overview.get('52WeekLow', 'N/A')
            
            processed_apis[index] = curr_api

        combined = zip(ticker, processed_apis.values())

    return render(request, 'add_stock.html', {'ticker': ticker, 'processed_apis': processed_apis, 'combined': combined})

def delete_stock(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()

    messages.success(request, ('Stock has been deleted'))

    return redirect(add_stock)