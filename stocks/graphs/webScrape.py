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

        company_name = parse.find('h1', {'class': "yf-xxbei9"}).text
        open = parse.find('fin-streamer', {'data-field': 'regularMarketOpen'}).text
        day_range = parse.find('fin-streamer', {'data-field': 'regularMarketDayRange'}).text
        price = parse.find('fin-streamer', {'class': "livePrice yf-1tejb6"}).text
        percent_change = parse.find('fin-streamer', {'class': "priceChange yf-1tejb6"}).text
        fiftytwo_week = parse.find('fin-streamer', {'data-field': 'fiftyTwoWeekRange'}).text
        market_cap = parse.find('fin-streamer', {'data-field': 'marketCap'}).text

        header_info = company_name.split("(")
        company_name = header_info[0]
        ticker = header_info[1].replace(")", "")

        range = day_range.split(" - ")
        low = range[0]
        high = range[1]

        fiftytwo_range = fiftytwo_week.split(" - ")
        fiftytwo_week_low = fiftytwo_range[0]
        fiftytwo_week_high = fiftytwo_range[1]

        info = {
            'company_name': company_name,
            'ticker': ticker,
            'open': open,
            'low': low,
            'high': high,
            'price': price,
            'percent_change': percent_change,
            'fiftytwo_week_low': fiftytwo_week_low,
            'fiftytwo_week_high': fiftytwo_week_high,
            'market_cap': market_cap
        }

        return info
            
            
    except Exception as e:
        return None

