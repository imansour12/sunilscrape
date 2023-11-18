import requests
from bs4 import BeautifulSoup

r = requests.get("https://www.ibpbooks.com/search/2311?q=+")
c = r.content

soup = BeautifulSoup(c, 'html.parser')

cards = soup.find_all('div', class_='card', style='border: none;')

for card in cards:
    card_body = card.find('div', class_='card-body')
    if card_body:
        a_tags = card_body.find_all('a')
        first_href = a_tags[0]['href'] if len(a_tags) > 0 else None
        title = a_tags[0].find('span').text if len(a_tags) > 0 else None
        price = a_tags[1].find('span').text if len(a_tags) > 1 else None
        author = card_body.find('span', class_='d-md-block d-sm-none d-none').text if card_body.find(
            'span', class_='d-md-block d-sm-none d-none') else None

        print("Title:", title)
        print("Price:", price)
        print("Author:", author)
        print("Href of first 'a' tag:", first_href)
        print("-----------------------")
