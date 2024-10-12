import requests
from bs4 import BeautifulSoup
from time import time

CACHE_DURATION = 3600

cache = {}


def get_stock_info(ticker):

    if ticker in cache and time() - cache[ticker]['timestamp'] < CACHE_DURATION:
        return cache[ticker]['data']

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0'}
    yahoo_url = f'https://finance.yahoo.com/quote/{ticker}/'
    try:
        
        req = requests.get(yahoo_url, headers=headers)
        req.raise_for_status()

        parse = BeautifulSoup(req.text, 'lxml')

        def find_element(selector, attribute=None):
            element = parse.select_one(selector)
            return element.get(attribute) if attribute else element.text.strip() if element else None

        title = parse.find('h1', {'class': "yf-xxbei9"}).text
        
        open = parse.find('fin-streamer', {'data-field': 'regularMarketOpen'}).text
        day_range = parse.find('fin-streamer', {'data-field': 'regularMarketDayRange'}).text
        price = parse.find('fin-streamer', {'data-field': 'regularMarketPrice'}).text
        fifty_two_week = parse.find('fin-streamer', {'data-field': 'fiftyTwoWeekRange'}).text
        #percent_change = parse.find('fin-streamer', {'data-field': "regularMarketChange"}).text

        company_name, ticker = title.split("(")
        ticker = ticker.rstrip(")")
        low, high = day_range.split(" - ")
        fifty_two_week_low, fifty_two_week_high = fifty_two_week.split(" - ")

        #if company_name contains ETF, then market_cap is not available
        if company_name.find("ETF") == -1: 
            market_cap = parse.find('fin-streamer', {'data-field': 'marketCap'}).text
        else:
            market_cap = '-'

        info = {
            'company_name': company_name,
            'ticker': ticker,
            'open': open,
            'low': low,
            'high': high,
            'price': price,
            'fifty_two_week_low': fifty_two_week_low,
            'fifty_two_week_high': fifty_two_week_high,
            'market_cap': market_cap,
        }

        cache[ticker] = {'data': info, 'timestamp': time()}
        
        return info
            
            
    except (requests.RequestException, AttributeError, ValueError) as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        return None
