from datetime import datetime

import requests
from ratelimit import limits, sleep_and_retry

import utils


def fetch():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,nl;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Dnt': '1',
        'Sec-Gpc': '1',
        'Upgrade-Insecure-Requests': '1',
        'referer': 'https://www.g2a.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.136 Safari/537.36'
    }

    @sleep_and_retry
    @limits(calls=1, period=1)
    def fetch_page(session, page):
        url = f"https://www.g2a.com/search/api/v2/products?itemsPerPage=50&include[0]=filters&currency=USD&isWholesale=false&f[device][0]=1118&f[drm][0]=1&f[regions][0]=8355&f[regions][1]=878&sort=best-match&category=189&price[max]=40&page={page}"
        return session.get(url, headers=headers)

    data = dict()

    with requests.session() as session:
        for page in range(1, 353):
            print(page, datetime.now())
            resp = fetch_page(session, page)
            if resp.ok:
                content = resp.json()
                games = content['data']['items']
                for game in games:
                    name = game['name']
                    name_lower = name.lower()
                    if 'random' in name_lower or 'edition' in name_lower:
                        continue
                    if name_lower.find('(pc)') == -1 or name_lower.find('steam') == -1:
                        i = max(name_lower.find('(pc)'), name_lower.find('steam'))
                    else:
                        i = min(name_lower.find('(pc)'), name_lower.find('steam'))
                    title = name[:i].replace('|', '').replace('  ', ' ').strip('- ')
                    appid = utils.find_appid(title)
                    if appid is None:
                        continue
                    data[appid] = (title, game['price'], 'g2a.com', game['href'])
            else:
                print('FAIL ', resp.status_code)
    return data.items()


if __name__ == '__main__':
    fetch()
