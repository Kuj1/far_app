import os
import random
import time

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service

from app.models import CardsSellBr
from app import db
from auth import login, password


# Constants
UA = UserAgent(verify_ssl=False)
URL = 'https://www.farpost.ru/primorskii-krai/realty/sell_business_realty/'

# Options
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument(f'--user-agent={UA.opera}')
options.add_argument('start-maximized')
options.add_argument('--headless')
options.add_argument('--enable-javascript')

# Proxy options (ip:port - personal for each parser)
proxy_options = {
    'proxy': {
        'https': f'http://{login}:{password}@109.248.7.208:11301'
    }
}

# Driver initial
s = Service(f'{os.getcwd()}/chromedriver')
driver = webdriver.Chrome(service=s, options=options, seleniumwire_options=proxy_options)

# Creating directory
dir_path = f'{os.getcwd()}/data'

if not os.path.exists(dir_path):
    os.mkdir(dir_path)


def get_data(url):
    try:
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        pagination = soup.find('span', class_='pagebarInner').text.split()[-2]

        if not pagination:
            pagination = soup.find('span', class_='pageCount').text.split()[1]

        for check_page in range(1, int(pagination) + 1):
            link_page = f'{URL}?page={check_page}'

            driver.get(link_page)

            card = BeautifulSoup(driver.page_source, 'html.parser')

            all_cards = card.find('table', class_='pageableContent').find_all('tr', class_='bull-item bull-item_inline -exact bull-item bull-item_inline')

            count = 1

            # Get completely page
            for check_link in all_cards:
                card_link = check_link.find('a', class_='bulletinLink bull-item__self-link auto-shy').get('href')
                views_info = check_link.find('span', class_='views nano-eye-text').text.strip()
                card_page = f'https://www.farpost.ru{card_link}'

                time.sleep(random.randint(10, 15))
                driver.get(card_page)

                link = BeautifulSoup(driver.page_source, 'html.parser')
                business_real_cards = link.find('a', class_='bzr-btn viewAjaxContacts viewbull-summary__button '
                                                            'bulletin-contacts-button bzr-btn_style_info '
                                                            'gtm__btn-contact-view').get('href')

                extend_link = f'https://www.farpost.ru{business_real_cards}'

                try:
                    photo_gallery = info.find('div', class_='imagesExBig').find_all('img')
                    photo_urls = []
                    for link in photo_gallery:
                        photo_link = link.get('src')
                        photo_urls.append(photo_link)
                    photo_raw = ' | '.join(photo_urls)
                except:
                    photo_raw = 'Нет данных'

                time.sleep(random.randint(30, 40))
                driver.get(extend_link)

                with open(f'{dir_path}/card_sell_br.html', 'w', encoding='utf-8') as doc:
                    doc.write(driver.page_source)

                with open(f'{dir_path}/card_sell_br.html', 'r') as src:
                    src = src

                    info = BeautifulSoup(src, 'html.parser')

                # Parsing data from page
                card_number_raw = info.find('span', class_='viewbull-bulletin-id__num').text.strip().replace('№', '')
                section_raw = 'Продажа помещений'
                title_raw = info.find('span', class_='inplace auto-shy').text

                date_post_raw = info.find('div', class_='viewbull-actual-date').text
                author_card_raw = info.find('span', class_='userNick auto-shy').text.strip()
                try:
                    region_address_raw = info.find('span', {'data-field': 'district'}).text.strip()
                except:
                    region_address_raw = 'Нет данных'

                try:
                    street_address_raw = info.find('span', {'data-field': 'street'}).text.strip()
                except:
                    street_address_raw = 'Нет данных'

                try:
                    size_raw = info.find('span', {'data-field': 'areaTotal'}).text.strip().replace(' кв. м.', '')
                except:
                    size_raw = 'Нет данных'

                try:
                    price_raw = info.find('span', {'itemprop': 'price'}).text.replace('₽', '')
                except:
                    price_raw = 'Нет данных'

                contacts_raw = info.find('div', class_='new-contacts dummy-listener_new-contacts').text.replace('\t',
                                            '').replace('\n', ' ')

                try:
                    card_descr = info.find('p', class_='inplace mod__label_up_down auto-shy').text.strip()
                except:
                    card_descr = 'Нет данных'

                # Add data in DB
                card = CardsSellBr(link_obj=card_page, views_info=views_info, description=card_descr,
                                   card_number=card_number_raw, section=section_raw, title=title_raw,
                                   photo=photo_raw, date_post=date_post_raw,
                                   author_card=author_card_raw, region_address=region_address_raw,
                                   street_address=street_address_raw,
                                   size=size_raw, price=price_raw, contacts=contacts_raw)
                db.session.add(card)
                db.session.commit()

                print(f'[INFO]: card #{count} - successfully parsed and insert into DB')

                count += 1

            print(f'[INFO]: all cards from {check_page} page - successfully parsed')

    except Exception as ex:
        print(f'[ERROR]: {ex}')

    finally:
        driver.close()
        driver.quit()


def main():
    get_data(URL)


if __name__ == "__main__":
    main()
