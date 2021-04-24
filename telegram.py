import requests
from dotenv import load_dotenv
load_dotenv()
import os
import urllib

def send(bot_message):
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    bot_chatID = os.environ['TELEGRAM_BOT_CHAT_ID']
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?parse_mode=HTML&chat_id=' + bot_chatID + '&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

def send_stock_newsletter(stocks):
  sorted_stocks = sorted(stocks, key=lambda k: k['priceTargetPct'], reverse=True)[:10]
  html = '';
  for i in range(len(sorted_stocks)):
    stock = sorted_stocks[i]
    html += create_html_for_stock(stock, i)
  return send(encode_html(html))


def create_html_for_stock(stock, i):
  # Telegram Bot API currently supports only <b>, <i>, <a>,<code> and <pre> tags, for HTML parse mode
  html = f'<b>{i+1}. <a href="https://www.finanzen.net{stock["href"]}">{stock["title"]}</a></b> | {stock["indexName"]} \n \n'
  props = [
    {"key": "priceTargetPct", "title": 'Price Target %'},
    {"key": "price", "title": 'Price'},
    {"key": "priceTarget", "title": 'Price Target'},
    {"key": "kgv", "title": 'KGV'},
    {"key": "dividend", "title": 'Dividend'},
    {"key": "dividendYield", "title": 'Dividend Yield'},
    ]
  for prop in props:
     value = stock[prop["key"]]
     html += f'<b>{prop["title"]}: </b> <i>{value}</i> \n'
  html += '\n'
  return html

def encode_html(encode_html):
  return urllib.parse.quote_plus(encode_html)

def test():
  send_stock_newsletter([
    {'href': '/aktien/allianz-aktie', 'title': 'allianz-aktie', 'isin': 'DE0008404005', 'wkn': '840400', 'id': '840400', 'priceTarget': 219.0, 'price': 216.1, 'priceTargetPct': 1.34, 'kgv': '12.40', 'kcv': '18.93', 'kbv':
  '18.93', 'dividend': '10.09', 'dividendYield': '4.68', 'indexName': 'DAX', 'indexHref': '/index/dax/30-werte'},
  {'href': '/aktien/cancom-aktie', 'title': 'cancom-aktie', 'isin': 'DE0005419105', 'wkn': '541910', 'id': '541910', 'priceTarget': 61.67, 'price': 51.06, 'priceTargetPct': 20.78, 'kgv': '28.49', 'kcv': '25.77', 'kbv': '25.77', 'dividend': '0.71', 'dividendYield': '1.38', 'indexName': 'TecDAX', 'indexHref': '/index/tecdax/werte'},
  {'href': '/aktien/aixtron-aktie', 'title': 'aixtron-aktie', 'isin': 'DE000A0WMPJ6', 'wkn': 'A0WMPJ', 'id': 'A0WMPJ', 'priceTarget': 20.3, 'price': 18.49, 'priceTargetPct': 9.79, 'kgv': '45.94', 'kcv': '1166.83', 'kbv': '1166.83', 'dividend': '0.11', 'dividendYield': '0.58', 'indexName': 'MDAX', 'indexHref': '/index/mdax/werte'},
  {'href': '/aktien/basf-aktie', 'title': 'basf-aktie', 'isin': 'DE000BASF111', 'wkn': 'BASF11', 'id': 'BASF11', 'priceTarget': 73.81, 'price': 70.19, 'priceTargetPct': 5.16, 'kgv': '20.15', 'kcv': '10.97', 'kbv': '10.97', 'dividend': '3.35', 'dividendYield': '4.77', 'indexName': 'DAX', 'indexHref': '/index/dax/30-werte'},
  {'href': '/aktien/aroundtown-aktie', 'title': 'aroundtown-aktie', 'isin': 'LU1673108939', 'wkn': 'A2DW8Z', 'id': 'A2DW8Z', 'priceTarget': 6.89, 'price': 6.14, 'priceTargetPct': 12.21, 'kgv': '12.28', 'kcv': '22.33', 'kbv': '22.33', 'dividend': '0.25', 'dividendYield': '4.02', 'indexName': 'MDAX', 'indexHref': '/index/mdax/werte' },
  {'href': '/aktien/adidas-aktie', 'title': 'adidas-aktie', 'isin': 'DE000A1EWWW0', 'wkn': 'A1EWWW', 'id': 'A1EWWW', 'priceTarget': 306.4, 'price': 268.15, 'priceTargetPct': 14.26, 'kgv': '139.35', 'kcv': '44.00', 'kbv': '44.00', 'dividend': '3.33', 'dividendYield': '1.23', 'indexName': 'DAX', 'indexHref': '/index/dax/30-werte'},
  {'href': '/aktien/adobe-aktie', 'title': 'adobe-aktie', 'isin': 'ADBE', 'wkn': '871981', 'id': '871981', 'priceTarget': 568.4, 'price': 422.2, 'priceTargetPct': 34.63, 'kgv': '47.10', 'kcv': '40.38', 'kbv': '40.38', 'dividend': '0.00', 'dividendYield': '-', 'indexName': 'NASDAQ 100', 'indexHref': '/index/nasdaq_100/werte'},
  {'href': '/aktien/alexion-aktie', 'title': 'alexion-aktie', 'isin': 'ALXN', 'wkn': '899527', 'id': '899527', 'priceTarget': 175.0, 'price': 139.34, 'priceTargetPct': 25.59, 'kgv': '12.47', 'kcv': '11.53', 'kbv': '11.53', 'dividend': '0.00', 'dividendYield': '-', 'indexName': 'NASDAQ 100', 'indexHref': '/index/nasdaq_100/werte'},
  {'href': '/aktien/airbus-aktie', 'title': 'airbus-aktie', 'isin': 'NL0000235190', 'wkn': '938914', 'id': '938914', 'priceTarget': 108.54, 'price': 98.94, 'priceTargetPct': 9.7, 'kgv': '66.31', 'kcv': '-13.97', 'kbv': '-13.97', 'dividend': '0.65', 'dividendYield': '0.65', 'indexName': 'MDAX', 'indexHref': '/index/mdax/werte'},
  {'href': '/aktien/apple-aktie', 'title': 'apple-aktie', 'isin': 'AAPL', 'wkn': '865985', 'id': '865985', 'priceTarget': 142.0, 'price': 109.58, 'priceTargetPct': 29.59, 'kgv': '35.60', 'kcv': '25.38', 'kbv': '25.38', 'dividend': '0.86', 'dividendYield': '0.65', 'indexName': 'Dow Jones', 'indexHref': '/index/dow_jones/werte'}
  ])

# test()