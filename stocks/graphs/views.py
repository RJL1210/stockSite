from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Stock
from .forms import StockForm
from django.contrib.auth.decorators import login_required
from . import webScrape

def home(request):

    if request.method == 'POST':
        ticker = request.POST['ticker']
        
        processed_api = webScrape.get_stock_info(ticker)
        
        if processed_api:
            # Check if the API call was successful
            api = "Success"
        else:
            #invalid ticker
            api = "Error..."
        return render(request, 'home.html', {'api': api, 'processed_api': processed_api})
    else:
        #default display
        return render(request, 'home.html', {'Ticker': ""})

    

def about(request):
    return render(request, 'about.html', {})

@login_required
def add_stock(request):

    if request.method == 'POST':
        form = StockForm(request.POST or None)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.user = request.user
            stock.save()
            messages.success(request, ('Stock has been added'))

            return redirect('add_stock')
    else:
        form = StockForm()
    
    # Retrieve all stocks for the current user
    stocks = Stock.objects.filter(user=request.user)
    processed_apis = {}
    for index, stock in enumerate(stocks):
        ticker = str(stock)
        try:
            # Attempt to get stock information from the web scraping function
            curr_api = webScrape.get_stock_info(ticker)
            if curr_api is None:
                raise Exception("API call was not successful")

        except Exception as e:
            # API call was not successful, so use default API (IBM)
            curr_api = {}

        processed_apis[index] = curr_api

    combined = zip(stocks, processed_apis.values())

    return render(request, 'add_stock.html', {'form': form, 'combined': combined})


@login_required
def delete_stock(request, stock_id):
    item = Stock.objects.get(pk=stock_id, user=request.user)
    item.delete()

    messages.success(request, ('Stock has been deleted'))

    return redirect(add_stock)

def index(request):
    return render(request, 'index.html', {})