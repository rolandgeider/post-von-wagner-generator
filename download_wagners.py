import requests
from bs4 import BeautifulSoup, SoupStrainer
import re
import json
from pathlib import Path

"""
Download all the currently available wagner texts from bild.de and reddit

Note that it seems that only the last 10 weeks of wagner texts are available on
the website. In order to properly train an AI, you need more, which means you
will have to regularly download the articles and then combine them (but since
you are already reading this, you are a hardcore fan of him and probably have a
tattoo on your arm, this shouldn't be a problem)

https://github.com/minimaxir/textgenrnn
"""


def process_input(article):
    """
    Processes and cleans up the articles.

    The result must be a single line (the complete file needs to have a single
    article per line)

    :param article: The article, as a string
    :return: the clean uped article
    """

    # Add space after periods. Some of the html text gets mangled up a bit from
    # and is removed in the next step
    article = article.replace('.', '. ')
    article = article.replace(',', ', ')
    article = article.replace('?', '? ')

    # Replace newlines, double spaces, etc
    article = " ".join(article.split())

    # Remove some text snippets
    items_to_remove = ["Die aktuelle Berichterstattung zum Thema finden Sie hier.",
                       "Die aktuelle Berichterstattung finden Sie hier.",
                       "Die Berichterstattung zum Thema finden Sie hier.",
                       "Die aktuelle Berichterstattung zum Thema lesen Sie hier.",
                       "Die aktuelle Berichterstattung zu diesem Thema finden Sie hier.",
                       "Mehr Informationen dazu findest du hier.",
                       "An dieser Stelle findest du Inhalte aus YouTube",
                       "Um mit Inhalten aus YouTube und anderen sozialen Netzwerken zu "
                       "interagieren oder diese darzustellen, brauchen wir deine Zustimmung.",
                       "soziale Netzwerke aktivieren",
                       "Ich bin damit einverstanden, dass mir Inhalte von Drittanbietern angezeigt "
                       "werden. ",
                       "Damit können personenbezogene Daten an Drittanbieter übermittelt werden. ",
                       "Dazu ist ggf. die Speicherung von Cookies auf deinem Gerät notwendig.",
                       "Mehr Informationen dazu findest du hier.",
                       ]
    for item in items_to_remove:
        article = article.replace(item, '')

    article = article.replace('HerzlichstFranz', 'Herzlichst Franz')
    article = article.replace('HerzlichstIhr', 'Herzlichst Ihr')
    article = article.replace('IhrF.', 'Ihr F.')

    article = article + "\n"

    return article


print("Processing reddit posts...")
print("==========================")
REDDIT_OVERVIEW = "https://www.reddit.com/r/PostVonWagner/.json?limit=1000"
page = requests.get(REDDIT_OVERVIEW, headers={'User-agent': 'Post von Wagner Bot 0.1'})
reddit_content = json.loads(page.content)
for post in reddit_content['data']['children']:
    post_id = post['data']['id']
    post_tile = post['data']['title']
    wagner_text = post['data']['selftext']

    print(f"   Processing post {post_id} - {post_tile}")
    with open(f"articles/{post_id}.txt", "w", encoding='utf8') as file:
        file.write(process_input(wagner_text))


print("Processing bild.de posts...")
print("===========================")
for i in range(0, 11):
    WAGNER_OVERVIEW = f"https://www.bild.de/themen/module/aktuell-reihe-15735732,contentContextId=17304844,inRegularien=false,page={i},parentWidth=10,view=content.bild.html"
    print(f"* page {i}")

    page = requests.get(WAGNER_OVERVIEW)
    soup = BeautifulSoup(page.content, 'html.parser')
    for link in BeautifulSoup(page.content, 'html.parser', parse_only=SoupStrainer('a')):
        if not link.has_attr('href'):
            continue

        article_link = link['href']
        if article_link == '#':
            continue

        print(f"   Processing... {article_link}")
        article_id = re.findall(r'\d+', article_link)[0]

        article_page = requests.get(f"https://www.bild.de/{article_link}")
        article_soup = BeautifulSoup(article_page.content, 'html.parser')

        # Articles are in a div wich class "txt"
        content_divs = article_soup.findAll('div', {"class": "txt"})

        # Write everything to files
        with open(f"articles/{article_id}.txt", "w", encoding='utf8') as file:
            file.write(process_input(content_divs[0].text))


# Collect all posts into a single file to train the AI with
print("Collecting all posts...")
print("=======================")
folder_listing = Path('articles').glob('*.txt')

with open(f"articles/wagner.out", "w", encoding='utf8') as collect_file:
    for file in folder_listing:
        with open(file, 'r', encoding='utf8') as current_wagner:
            collect_file.write(process_input(current_wagner.read()))


print("~~~ DONE! ~~~")
print("=============")
