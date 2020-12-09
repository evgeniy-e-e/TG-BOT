import re
import requests
import os.path
from bs4 import BeautifulSoup as BS

response = requests.get('https://stopgame.ru/review/new')
html = BS(response.content, features='html.parser')

def parse_href(href):
    result = re.match(r'\/show\/(\d+)', href)
    return result.group(1)

def get_lastkey():
    response = requests.get('https://stopgame.ru/review/new')
    html = BS(response.content, 'html.parser')

    items = html.select('.tiles > .items > .item > a')
    return parse_href(items[0]['href'])

    print(items)
