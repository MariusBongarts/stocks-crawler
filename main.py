import requests
base_url = "https://www.finanzen.net"
from bs4 import BeautifulSoup
from db import write
from telegram import send_stock_newsletter

# db = FireStoreDb()

def get_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')

def get_table(soup):
    return soup.select('#index-list-container')[0]

def format_euro(price):
  price = price.split('EUR')[0]
  price_euro = price.split(',')[0].replace('.', '')
  price_cent = price.split(',')[1]
  return float(f'{price_euro}.{price_cent}')

def get_stock_info(href):
    stock = {}

    soup = get_soup(base_url + href)
    instrument_id = soup.select('.instrument-id span[cptxt="WKN"]')[0].parent.text.split()
    stock["href"] = href
    stock["title"] = href.split('/')[len(href.split('/'))-1]
    stock["isin"] = instrument_id[len(instrument_id) - 1]
    stock["wkn"] = instrument_id[1]
    stock["id"] = stock["wkn"]
    price_target_container = soup.select('.iconTacho')[0].parent
    stock["priceTarget"] = format_euro(price_target_container.select('strong')[1].text)
    price = format_euro(soup.select('.quotebox div')[0].text)
    stock["price"] = price
    stock["priceTargetPct"] = round((stock["priceTarget"] - stock["price"]) / stock["price"] * 100, 2)
    stock["kgv"] = format_euro(soup.select('div[title="Kurs/Gewinn Verhältnis"]')[0].parent.parent.select('td')[1].text)
    stock["kcv"] = format_euro(soup.select('div[title="Kurs/Cashflow Verhältnis"]')[0].parent.parent.select('td')[1].text)
    stock["kbv"] = format_euro(soup.select('div[title="Kurs/Cashflow Verhältnis"]')[0].parent.parent.select('td')[1].text)
    stock["dividend"] = format_euro(soup.select('.table-quotes')[1].select('.table-responsive .table')[0].select('tr')[1].select('td')[3].text)
    stock["dividendYield"] = format_euro(soup.select('.table-quotes')[1].select('.table-responsive .table')[0].select('tr')[2].select('td')[3].text)
    return stock

table = get_table(get_soup(base_url + "/index/dax/30-werte"))

stocks = []

# Get different markets
indexs = table.select('.box-nav li a')
for index in indexs:
    index_href = index.get('href')
    index_name = index.text
    print('############## ' + index_name + ' ##############')

    table = get_table(get_soup(base_url + index_href))
    rows = table.select('tr')

    for row in rows:
        try:
            a_element = row.select('td')[0].select('a')[0]
        except Exception as e:
            print(e)
            a_element = None
            pass
        if a_element is not None:
          try:
            href = a_element.get('href')
            # Check if stock has already been crawled
            if href not in list(map(lambda x: x["href"], stocks)):
              text = a_element.text
              stock = get_stock_info(href)
              stock["indexName"] = index_name
              stock["indexHref"] = index_href
              print(stock)
              write("stocks", stock)
              stocks.append(stock)
          except Exception as e:
            print(e)
            pass

send_stock_newsletter(stocks)