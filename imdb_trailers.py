import re
import requests
import os.path
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse



class IMDB:
    host = "https://www.imdb.com"
    url = "https://www.imdb.com/trailers/?ref_=nv_mv_tr"
    lastkey = ""
    lastkey_file = ""

    def __init__(self, lastkey_file):
        self.lastkey_file = lastkey_file

        if(os.path.exists(lastkey_file)):
            self.lastkey = open(lastkey_file,'r').read()
        else:
            f = open(lastkey_file,'w')
            self.lastkey = self.get_lastkey()
            f.write(self.lastkey)
            f.close()

    def new_trailers(self):
        r = requests.get(self.url)
        html = BS(r.content,'html.parser')
        new = []
        items = html.select('.ipc-poster > .ipc-lockup-overlay')
        for i in items:
            key = self.parse_href(i('href'))
            if(self.lastkey < key):
                new.append(i('href'))
        return new

    def trailer_info(self, uri):
        link = self.host + uri
        r = requests.get(link)
        html = BS(r.content, 'html.parser')
        poster = html.select('.ipc-media > .ipc-image')[0]['src']

        # remels = gfgdfggf
        info = {
            "id" : self.parse_href(uri),
            "title" : html.select('.ipc-poster-card__title > a')[0].text,
            "link" : link,
            "image" : poster.group(1)
        }
        return info

    def download_image(self, url):
        r = requests.get(url, allow_redirects=True)
        a = urlparse(url)
        filename = os.path.basename(a.path)
        open(filename,'wb').write(r.content)
        return filename

    def get_lastkey(self):
        r = requests.get(self.url)
        html = BS(r.content, "html.parser")
        items = html.select('.ipc-poster > .ipc-lockup-overlay')
        return self.parse_href(items[0]['href'])

    def parse_href(self, href):
        result = re.match(r'\/video\/vi\d+\?ref_=vi_tr_tr_vp_(\d+)', href)
        return result.group(1)

    def update_lastkey(self,new_key):
        self.lastkey = new_key

        with open(self.lastkey_file, 'r+') as f:
            data = f.read()
            f.seek(0)
            f.write(str(new_key))
            f.truncate()
        return new_key
