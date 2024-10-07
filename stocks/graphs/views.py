from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .models import Stock
from .forms import StockForm
from django.contrib.auth.decorators import login_required

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
                #out of calls
                processed_api['outOfCalls'] = True
                processed_api['symbol'] = 'IBM'
                processed_api['open'] = '219.5000'
                processed_api['high'] = "222.8300"
                processed_api['low'] = "219.2700"
                processed_api['price'] = "222.7200"

                processed_api['marketcap'] = readNumber("202403856000")
                processed_api['companyname'] = "International Business Machines"
                processed_api['52weekhigh'] = "224.15"
                processed_api['52weeklow'] = "130.68"


            

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

@login_required
def add_stock(request):
    import requests
    import json

    if request.method == 'POST':
        form = StockForm(request.POST or None)
        if form.is_valid():
            stock = form.save(commit = False)
            stock.user = request.user
            stock.save()
            messages.success(request, ('Stock has been added'))
            return redirect('add_stock')
    else:
        form = StockForm()
    
    stocks = Stock.objects.filter(user=request.user)
    processed_apis = {}
    for index, stock in enumerate(stocks):
        ticker = stock
        try:
            api_request = requests.get(f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={context['api_key']}")
            api = api_request.json()
            overview_request = requests.get(f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={context['api_key']}")
            overview = overview_request.json()

            curr_api = {}
            curr_api['symbol'] = ticker
            curr_api['open'] = api['Global Quote'].get('02. open', 'N/A')
            curr_api['high'] = api['Global Quote'].get('03. high', 'N/A')
            curr_api['low'] = api['Global Quote'].get('04. low', 'N/A')
            curr_api['price'] = api['Global Quote'].get('05. price', 'N/A')
            curr_api['change'] = api['Global Quote'].get('09. change', 'N/A')
            curr_api['change percent'] = api['Global Quote'].get('10. change percent', 'N/A')
            curr_api['marketcap'] = readNumber(overview.get('MarketCapitalization', 'N/A'))
            curr_api['companyname'] = overview.get('Name', 'N/A')
            curr_api['52weekhigh'] = overview.get('52WeekHigh', 'N/A')
            curr_api['52weeklow'] = overview.get('52WeekLow', 'N/A')
        except Exception as e:
            # API call was not successful, so use default API (IBM)
            curr_api = {}
            curr_api['symbol'] = 'IBM'
            curr_api['open'] = '219.5000'
            curr_api['high'] = "222.8300"
            curr_api['low'] = "219.2700"
            curr_api['price'] = "222.7200"
            curr_api['marketcap'] = readNumber("202403856000")
            curr_api['companyname'] = "International Business Machines"
            curr_api['52weekhigh'] = "224.15"
            curr_api['52weeklow'] = "130.68"

        processed_apis[index] = curr_api

    combined = zip(stocks, processed_apis.values())

    return render(request, 'add_stock.html', {'form': form, 'combined': combined})


@login_required
def delete_stock(request, stock_id):
    item = Stock.objects.get(pk=stock_id, user=request.user)
    item.delete()

    messages.success(request, ('Stock has been deleted'))

    return redirect(add_stock)