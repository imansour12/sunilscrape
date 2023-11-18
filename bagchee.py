import requests
from bs4 import BeautifulSoup
import csv
import concurrent.futures
import fasteners


def scrape_page(page_number):
    base_url = "https://www.bagchee.com/books/?page="
    url = f"{base_url}{page_number}"

    r = requests.get(url)
    c = r.content

    soup = BeautifulSoup(c, "html.parser")
    ul_element = soup.find('ul', class_='product-ul')

    data = []

    if ul_element:
        li_elements = ul_element.find_all('li')
        for li in li_elements:
            row = []
            price_span = li.find('span', class_='price')
            if price_span:
                try:
                    price = price_span.text.strip()
                    price = price[:-2]
                    price = float(price) * 83.29
                    price = round(price, 2)
                except ValueError:
                    price = 0.0
                price = f"₹ {price}"
                row.append(price)

            h2_element = li.find('h2')
            if h2_element:
                a_tag = h2_element.find('a')
                if a_tag:
                    href = a_tag.get('href')
                    text = a_tag.text.strip()
                    row.append(text)
                    row.append(href)

            if row:
                data.append(row)

    return data


def write_to_csv(data):
    with fasteners.InterProcessLock('output.csv.lock'):
        with open('output.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(data)


def scrape_and_write(page_number):
    data = scrape_page(page_number)
    if data:
        write_to_csv(data)


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        pages = range(1, 4853)  # Loop through pages 1 to 4852
        executor.map(scrape_and_write, pages)


if __name__ == "__main__":
    main()
