import json
from datetime import datetime

import undetected_chromedriver as uc
from ratelimit import limits, sleep_and_retry
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import utils


def fetch():
    @sleep_and_retry
    @limits(calls=1, period=4.5)
    def fetch_page(page=0):
        driver.get(
            f'https://www.humblebundle.com/store/api/search?sort=alphabetical&platform=windows&drm=steam&page={page}&request=1')
        # print(driver.page_source)
        tag = driver.find_element(By.TAG_NAME, 'body')
        content = json.loads(tag.text)
        driver.back()
        return content

    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    driver = uc.Chrome(options=chrome_options)
    content = fetch_page()
    data = dict()
    pages = content['num_pages']
    for page in range(1, pages + 1):
        print(f"\r{page} / {pages} {datetime.now()}", end='\n')
        content = fetch_page(page)
        for product in content['results']:
            if product['cta_badge'] != 'coming_soon':
                # print(product['human_name'])
                price = product['current_price']['amount']
                title = product['human_name']
                href = product['human_url']
                appid = utils.find_appid(title)
                if appid is None:
                    continue
                data[appid] = (title, price, 'humblebundle.com', href)

    return data.items()


if __name__ == '__main__':
    fetch()
