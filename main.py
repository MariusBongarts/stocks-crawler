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
    stock["href"] = href
    stock["title"] = href.split('/')[len(href.split('/'))-1]
    stock["isin"] = instrument_id[len(instrument_id) - 1]
    stock["wkn"] = instrument_id[1]
    stock["id"] = stock["wkn"]
    price_target_container = soup.select('.iconTacho')[0].parent
    stock["priceTargetPct"] = float(price_target_container.select('strong')[0].text.replace(',','.').replace('%',''))
    stock["priceTarget"] = float(price_target_container.select('strong')[1].text.replace(',','.'))
    stock["price"] = float(soup.select('.quotebox div')[0].text.split('EUR')[0].replace(',','.'))
    stock["kgv"] = soup.select('div[title="Kurs/Buchwert Verhältnis"]')[0].parent.parent.select('td')[1].text.replace(',','.')
    stock["kcv"] = soup.select('div[title="Kurs/Cashflow Verhältnis"]')[0].parent.parent.select('td')[1].text.replace(',','.')
    stock["kbv"] = soup.select('div[title="Kurs/Cashflow Verhältnis"]')[0].parent.parent.select('td')[1].text.replace(',','.')
    stock["dividend"] = soup.select('.table-quotes')[1].select('.table-responsive .table')[0].select('tr')[1].select('td')[3].text.replace(',','.')
    stock["dividendYield"] = soup.select('.table-quotes')[1].select('.table-responsive .table')[0].select('tr')[2].select('td')[3].text.replace(',','.')
    print(stock)
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
            stock["indexName"] = index_name
            stock["indexHref"] = index_href
            write("stocks", stock)
          except:
            pass