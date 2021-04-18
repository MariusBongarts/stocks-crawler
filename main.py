import requests
base_url = "https://www.finanzen.net"
from bs4 import BeautifulSoup


def get_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')

def get_table(soup):
    table = soup.select('.table-quotes')[0]
    return table

def get_stock_info(href):
    soup = get_soup(base_url + href)
    price_target_container = soup.select('.iconTacho')[0].parent
    price_target_percentage = price_target_container.select('strong')[0].text
    price_target_absolute = price_target_container.select('strong')[1].text
    stock = {}
    stock["href"] = href
    stock["price_target_percentage"] = price_target_percentage
    stock["price_target_absolute"] = price_target_absolute
    return stock

table = get_table(get_soup(base_url + "/index/dax/30-werte"))

# Get different markets
indexs = table.select('.box-nav li a')
for index in indexs:
    href = index.get('href')
    title = index.text
    print('############## ' + title + ' ##############')

    table = get_table(get_soup(base_url + href))
    rows = table.select('tr')

    for row in rows:
        try:
            a_element = row.select('td')[0].select('a')[0]
        except:
            a_element = None
            pass
        if a_element is not None:
            href = a_element.get('href')
            print(href)
            text = a_element.text
            stock = get_stock_info(href)
            print(stock)