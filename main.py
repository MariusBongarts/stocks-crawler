import requests
base_url = "https://www.finanzen.net"
from bs4 import BeautifulSoup
from db import write

# db = FireStoreDb()

def get_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')

def get_table(soup):
    table = soup.select('.table-quotes')[0]
    return table

def get_stock_info(href):
    stock = {}

    soup = get_soup(base_url + href)
    instrument_id = soup.select('.instrument-id span[cptxt="WKN"]')[0].parent.text.split()
    stock["isin"] = instrument_id[len(instrument_id) - 1]
    stock["wkn"] = instrument_id[1]
    stock["id"] = stock["wkn"]
    price_target_container = soup.select('.iconTacho')[0].parent
    stock["price_target_percentage"] = float(price_target_container.select('strong')[0].text.replace(',','.').replace('%',''))
    stock["price_target_absolute"] = float(price_target_container.select('strong')[1].text.replace(',','.'))
    stock["price"] = float(soup.select('.quotebox div')[0].text.split('EUR')[0].replace(',','.'))
    return stock

table = get_table(get_soup(base_url + "/index/dax/30-werte"))

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
        except:
            a_element = None
            pass
        if a_element is not None:
          try:
            href = a_element.get('href')
            text = a_element.text
            stock = get_stock_info(href)
            stock["index_name"] = index_name
            stock["index_href"] = index_href
            write("stocks", stock)
          except:
            pass