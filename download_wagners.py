import requests
from bs4 import BeautifulSoup, SoupStrainer
import re

"""
Download all the currently available wagner texts from bild.de

Note that it seems that only the last 10 weeks of wagner texts are available on
the website. In order to properly train an AI, you need more, which means you
will have to regularly download the articles and then combine them (but since
you are already reading this, you are a hardcore fan of him and probably have a
tattoo on your arm, this shouldn't be a problem)
"""

for i in range(0, 11):

    WAGNER_OVERVIEW = f"https://www.bild.de/themen/module/aktuell-reihe-15735732,contentContextId=17304844,inRegularien=false,page={i},parentWidth=10,view=content.bild.html"
    print(f"PAGE {i}")
    print("----------")

    page = requests.get(WAGNER_OVERVIEW)
    soup = BeautifulSoup(page.content, 'html.parser')
    for link in BeautifulSoup(page.content, 'html.parser', parse_only=SoupStrainer('a')):
        if not link.has_attr('href'):
            continue

        article_link = link['href']
        if article_link == '#':
            continue

        print(f"processing... {article_link}")
        article_id = re.findall(r'\d+', article_link)[0]

        article_page = requests.get(f"https://www.bild.de/{article_link}")
        article_soup = BeautifulSoup(article_page.content, 'html.parser')

        # Articles are in a div wich class "txt"
        content_divs = article_soup.findAll('div', {"class": "txt"})

        # Write everything to files
        with open(f"articles/{article_id}.txt", "w", encoding='utf8') as file:
            file.write(content_divs[0].text)

        # And everything to one file
        with open(f"articles/wagner.txt", "a", encoding='utf8') as file:
            file.write(content_divs[0].text)
