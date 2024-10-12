import requests
from bs4 import BeautifulSoup


def get_stock_info(ticker):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0'}
    try:
        yahoo_url = 'https://finance.yahoo.com/quote/' + ticker + '/'

        
        req = requests.get(yahoo_url, headers=headers)
        if (req.status_code != 200):
            return None

        parse = BeautifulSoup(req.text, 'html.parser')

        title = parse.find('h1', {'class': "yf-xxbei9"}).text
        open = parse.find('fin-streamer', {'data-field': 'regularMarketOpen'}).text
        day_range = parse.find('fin-streamer', {'data-field': 'regularMarketDayRange'}).text
        price = parse.find('fin-streamer', {'data-field': 'regularMarketPrice'}).text
        fifty_two_week = parse.find('fin-streamer', {'data-field': 'fiftyTwoWeekRange'}).text
        #percent_change = parse.find('fin-streamer', {'data-field': "regularMarketChange"}).text

        header_info = title.split("(")
        company_name = header_info[0]
        ticker = header_info[1].replace(")", "")

        if company_name.find("ETF") == -1: 
            market_cap = parse.find('fin-streamer', {'data-field': 'marketCap'}).text
            stock = True
        else:
            market_cap = '-'
            stock = False

        header_info = title.split("(")
        company_name = header_info[0]
        ticker = header_info[1].replace(")", "")

        range = day_range.split(" - ")
        low = range[0]
        high = range[1]

        fifty_two_range = fifty_two_week.split(" - ")
        fifty_two_week_low = fifty_two_range[0]
        fifty_two_week_high = fifty_two_range[1]

        info = {
            'company_name': company_name,
            'ticker': ticker,
            'open': open,
            'low': low,
            'high': high,
            'price': price,
            #'percent_change': percent_change,
            'fifty_two_week_low': fifty_two_week_low,
            'fifty_two_week_high': fifty_two_week_high,
            'market_cap': market_cap,
            'stock': stock
        }

        return info
            
            
    except Exception as e:
        return None

