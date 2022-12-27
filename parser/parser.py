"""
Some docstring
"""

import re
import time
import requests
from bs4 import BeautifulSoup
from urllib3 import Retry
from requests.adapters import HTTPAdapter


def parse_farmani(url_to_parse: str):
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    article_request = session.get(url_to_parse, verify=False)

    if not article_request.ok:
        print('Could not parse!')
        return article_request.ok

    time.sleep(2)
    article_soup = BeautifulSoup(article_request.text, features="lxml")
    counter = 3
    drugs_found = []
    for block in article_soup.find_all(
            'div', attrs={"class": "list_item_wrapp item_wrap item"}):
        if counter == 0:
            break
        data = []
        try:
            title = block.find('div', attrs={
                "class": "item-title"}).find('span').text.replace('\t', '').replace('\n', '')
            country = block.find('div', attrs={
                "class": "wrap-country"}).text.replace('\t', '').replace('\n', '')
            manufacturer = block.find('div', attrs={
                "class": "wrap-manufacturer"}).text.replace('\t', '').replace('\n', '')
        except AttributeError:
            continue
        try:
            price = block.find('span', attrs={
                "class": "default_price"}).text.replace('\t', '').replace('\n', '')
            print(price)
        except AttributeError:
            price = block.find('span', attrs={
                "class": "element_new_price"}).text.replace('\t', '').replace('\n', '')
            print(price)
        data.append(title)
        data.append(country)
        data.append(manufacturer)
        data.append(price)
        drugs_found.append(data)
        counter -= 1
    print(drugs_found)
    return drugs_found


if __name__ == "__main__":
    parse_farmani('https://farmani.ru/search/?q=смекта')
