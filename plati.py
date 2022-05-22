import html
import re
from datetime import datetime

import requests

import utils


def fetch():
    query = 'steam key'
    url = f"http://www.plati.io/api/search.ashx?visibleOnly=true&pagesize=500&response=json&query={query}&pagenum=1"
    json_resp = requests.get(url).json()
    pages = json_resp['Totalpages']
    data = dict()

    with requests.session() as session:
        for page in range(1, pages + 1):
            print(f"\r{page} / {pages} {datetime.now()}", end='\n')
            url = f"https://www.plati.io/api/search.ashx?visibleOnly=true&pagesize=500&response=json&query={query}&pagenum={page}"
            json_resp = session.get(url).json()

            for item in json_resp['items']:
                if item['seller_id'] == 319113 and not 'random' in item['name_eng'].lower():
                    description = html.unescape(item['description'])
                    match = re.search(r'(?i)(?:store.steampowered.com|steamcommunity.com)/app/(\d*)', description)
                    if match is None:
                        continue
                    appid = int(match.groups(0)[0])
                    title = utils.find_title(appid)
                    data[appid] = (title, item['price_usd'], 'plati.ru', item['url'])

    return data.items()


if __name__ == '__main__':
    fetch()
