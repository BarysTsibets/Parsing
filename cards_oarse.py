import requests
from bs4 import BeautifulSoup
import csv

HOST = 'https://minfin.com.ua/'
URL = 'https://minfin.com.ua/cards/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9 ',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/84.0.4147.89 Mobile Safari/537.36 '
}


def get_html(url, params=""):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

#
# def pages_count(html):
#     soup = BeautifulSoup(html, "html.parser")
#     pagination = soup.find_all("li", class_="active").get_text()
#     print(pagination)


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all('div', class_="product-item")
    cards = []

    for item in items:
        cards.append(
            {
                'title': item.find("div", class_="title").get_text(strip=True),
                'link product': HOST + item.find("div", class_="title").find("a").get("href"),
                'brand': item.find("div", class_="brand").get_text(strip=True),
                'card_img': HOST + item.find("div", class_="image").find("img").get("src"),
            }
        )
    return cards


def parser():
    PAGINATION = int(input("How many page do u want to parse ? ").strip())
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range (1, PAGINATION + 1):
            print(f"Parsing page number : {page}...")
            html = get_html(URL, params={"page": page})
            cards.extend(get_content(html.text))
        print(cards)
    else:
        print("error")

parser()


# html = get_html(URL)
# print(get_content(html.text))
