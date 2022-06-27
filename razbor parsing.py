import requests
from bs4 import BeautifulSoup
import csv

URL = "https://www.mashina.kg/search/all/"


def get_html(url: str):
    html = requests.get(url=url)
    return html.text


def get_last_page(html):
    soup = BeautifulSoup(html, "lxml")
    pagination = soup.find("ul", class_ = "pagination").find_all('a', class_='page-link')
    last = pagination[-4].text
    return int(last)



def write_to_csv(data: list) -> None:
    with open('mashina.kg.csv', "a") as file:
        writer = csv.writer(file, delimiter="/")
        writer.writerow(["title", "price", "description", "image"])
        for item in data:
            writer.writerow([item.get("title"), item.get("price"), item.get("description"), item.get("image")])


DATA = []


def get_data(html):
    soup = BeautifulSoup(html, "lxml")
    cars = soup.find("div", class_="table-view-list").find_all("a")
    for car in cars:
        try:
            title = car.find("h2", class_="name").text.strip()
            # print(title)
        except:
            title = "---"
        try:
            price = car.find("strong").text
            # print(price)
        except:
            price = "---"
        try:
            desc = car.find("p", class_="year-miles").text.strip()
            desc2 = car.find('p', class_= 'body-type').text.strip()
            desc3 = car.find('p', class_= 'volume').text.strip()
            description = desc + desc2 + desc3
            # print(description)
        except:
            desc = "---"
            desc2 = "---"
            desc3 = "---"
        try:
            image = car.find('div', class_="thumb-item-carousel").find("img").get("data-src")
            # print(image)
        except:
            image = "---"
        dep = {"title": title, "price": price, "description": description, "image": image}
        DATA.append(dep)


def main():
    html = get_html(URL)
    for i in range(1, get_last_page(html)):
        URl_PAGE = URL + "?page=" + str(i)
        html = get_html(url=URl_PAGE)
        get_data(html=html)
    write_to_csv(DATA)


main()

html = get_html(url=URL)
get_last_page(html)

get_data(html)
write_to_csv(DATA)