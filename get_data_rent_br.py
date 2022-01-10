import os
import random
import time

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from app.models import CardsRentBr
from app import db


# Constants
UA = UserAgent(verify_ssl=False)
URL = 'https://www.farpost.ru/primorskii-krai/realty/rent_business_realty/'

# Options
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument(f'--user-agent={UA.opera}')
options.add_argument('start-maximized')
options.add_argument('--headless')
options.add_argument('--enable-javascript')

# Driver initial
s = Service(f'{os.getcwd()}/chromedriver')
driver = webdriver.Chrome(service=s, options=options)

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

            all_cards = card.find('table', class_='pageableContent').find_all('tr', class_='-exact bull-item '
                                                                                           'bull-item_inline')

            count = 1

            # Get completely page
            for check_link in all_cards:
                card_link = check_link.find('a', class_='bulletinLink bull-item__self-link auto-shy').get('href')
                card_page = f'https://www.farpost.ru{card_link}'

                time.sleep(random.randint(30, 60))
                driver.get(card_page)

                link = BeautifulSoup(driver.page_source, 'html.parser')
                business_real_cards = link.find('a', class_='bzr-btn viewAjaxContacts viewbull-summary__button '
                                                            'bulletin-contacts-button bzr-btn_style_info '
                                                            'gtm__btn-contact-view').get('href')

                extend_link = f'https://www.farpost.ru{business_real_cards}'

                time.sleep(random.randint(30, 60))
                driver.get(extend_link)

                with open(f'{dir_path}/card_rent_br.html', 'w', encoding='utf-8') as doc:
                    doc.write(driver.page_source)

                with open(f'{dir_path}/card_rent_br.html', 'r') as src:
                    src = src

                    info = BeautifulSoup(src, 'html.parser')

                # Parsing data from page
                card_number_raw = info.find('span', class_='viewbull-bulletin-id__num').text.strip().replace('№', '')
                section_raw = 'Аренда помещений'
                title_raw = info.find('span', class_='inplace auto-shy').text

                try:
                    photo_gallery = info.find('div', class_='imagesExBig').find_all('img')
                    photo_urls = []
                    for link in photo_gallery:
                        photo_link = link.get('src')
                        photo_urls.append(photo_link)
                    photo_raw = ' | '.join(photo_urls)
                except:
                    photo_raw = 'Нет данных'

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

                try:
                    price_for_what_raw = info.find('span', 'viewbull-summary-price__quantity').text
                except:
                    price_for_what_raw = 'Нет данных'

                contacts_raw = info.find('div', class_='new-contacts dummy-listener_new-contacts').text.replace('\t',
                                                                                                                '').\
                    replace('\n', ' ')

                # Add data in DB
                card = CardsRentBr(card_number=card_number_raw, section=section_raw, title=title_raw,
                                   photo=photo_raw, date_post=date_post_raw,
                                   author_card=author_card_raw, region_address=region_address_raw,
                                   street_address=street_address_raw,
                                   size=size_raw, price=price_raw,
                                   price_for_what=price_for_what_raw, contacts=contacts_raw)
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
