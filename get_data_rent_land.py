import os
import random
import time

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from app.models import CardsRentLand
from app import db

# Constants
UA = UserAgent(verify_ssl=False)
URL = 'https://www.farpost.ru/primorskii-krai/realty/land-rent/'

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

                with open(f'{dir_path}/card_rent_land.html', 'w', encoding='utf-8') as doc:
                    doc.write(driver.page_source)

                with open(f'{dir_path}/card_rent_land.html', 'r') as src:
                    src = src

                    info = BeautifulSoup(src, 'html.parser')

                # Parsing data from page
                card_number_raw = info.find('span', class_='viewbull-bulletin-id__num').text.strip().replace('№', '')
                section_raw = 'Продажа земельного участка'
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
                    placement_raw = info.find('span', {'data-field': 'landDistrict'}).text.strip()
                except:
                    placement_raw = 'Нет данных'

                try:
                    size_raw = info.find('span', {'data-field': 'areaTotal'}).text.strip().replace(' кв. м.', '')
                except:
                    size_raw = 'Нет данных'

                try:
                    price_raw = info.find('span', {'itemprop': 'price'}).text.replace('₽', '')
                    price_for_what_raw = info.find('span', 'viewbull-summary-price__quantity').text
                except:
                    price_raw = 'Нет данных'
                    price_for_what_raw = 'Нет данных'

                try:
                    status_raw = info.find('span', {'data-field': 'realtyStatus'}).text.strip()
                except:
                    status_raw = 'Нет данных'

                try:
                    restrictions_raw = info.find('span', {'data-field': 'restrictions'}).text.strip()
                except:
                    restrictions_raw = 'Нет данных'

                try:
                    cadastr_number_f_raw = info.find('span', {'data-field': 'cadastreNumber'}).contents[0].strip()
                except:
                    cadastr_number_f_raw = 'Нет данных'

                try:
                    cadastr_number_s_raw = info.find('span', {'data-field': 'cadastreNumber'}).contents[-1].strip()
                except:
                    cadastr_number_s_raw = 'Нет данных'

                try:
                    electricity_raw = info.find('span', {'data-field': 'electricity'}).text.strip()
                except:
                    electricity_raw = 'Нет данных'

                try:
                    water_raw = info.find('span', {'data-field': 'water'}).text.strip()
                except:
                    water_raw = 'Нет данных'

                try:
                    roads_raw = info.find('span', {'data-field': 'roads'}).text.strip()
                except:
                    roads_raw = 'Нет данных'

                contacts_raw = info.find('div', class_='new-contacts dummy-listener_new-contacts').text.replace('\t',
                                                                                                '').replace('\n', ' ')
                # Add data in DB
                card = CardsRentLand(link_obj=card_page, card_number=card_number_raw, section=section_raw, title=title_raw,
                                     photo=photo_raw, date_post=date_post_raw,
                                     author_card=author_card_raw, placement=placement_raw,
                                     size=size_raw, price=price_raw, price_for_what=price_for_what_raw,
                                     status=status_raw, restrictions=restrictions_raw,
                                     cadastr_number_f=cadastr_number_f_raw,
                                     cadastr_number_s=cadastr_number_s_raw, electricity=electricity_raw,
                                     water=water_raw,
                                     roads=roads_raw, contacts=contacts_raw)
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
