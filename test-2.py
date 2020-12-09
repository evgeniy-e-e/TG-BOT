import re
import requests
import os.path
from bs4 import BeautifulSoup as BS

response = requests.get('https://www.imdb.com/trailers/?ref_=nv_mv_tr')
html = BS(response.content, features='html.parser')
poster = html.select('.ipc-poster > .ipc-lockup-overlay')

print(poster[0]['href'])
# poster = re.match(r'src=\"(https?://[^\r\n\t\f\v\"]+)\"', html.select('.ipc-media > .ipc-image')[0]['src'])
# print(poster)

