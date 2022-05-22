import requests
from bs4 import BeautifulSoup as bs


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
        'referer': 'https://cheapkeys.ovh/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.136 Safari/537.36'
    }

    url = "http://cheapkeys.ovh/table.php"
    content = requests.get(url, headers=headers).text
    page_soup = bs(content, "html.parser")
    div = page_soup.select('div#tables')[0]
    trows = div.select('tr')
    data = dict()
    for tr in trows:
        tds = tr.findAll('td')[1:3]
        title = tds[0].text
        appid = tds[0].a.get('href').split('/')[-2]
        price = tds[1].text.strip()
        link = tds[1].a.get('href').split('?')[0]
        store = link.split('/')[2]
        data[appid] = (title, price, store, link)

    return data.items()


if __name__ == '__main__':
    fetch()
