import requests
from bs4 import BeautifulSoup, Tag
import pandas as pd
from cmath import log10
import re

# Utility functions 
def get3digitFormat(num):
    return f"{num:03d}"

def text_to_image_link(text):
    return text.replace(" ", "%20")

# ACTUAL DATA GETTERS
def get_content(p_soup):
    """ transforms effect description from a card to understandable text

    Args:
        p_soup (String): HTML p container with text and possibly images

    Returns:
        String: readable effect description
    """
    text_parts = []

    for content in p_soup.contents:
        if isinstance(content, Tag):
            if content.name == 'img':
                text_parts.append(dices_adapter(content['title']))
            elif content.name == 'strong':
                text_parts.append(content.get_text(strip=True))
        else:
            text_parts.append(content.strip())

    return ' '.join(text_parts)

def dices_adapter(dice):
    str(dice).replace(" ", "")
    match dice :
        case "diceb":
            return "defense die"
        case _:
            return dice


# TODO : automatic page making
def make_web_page(card_data):
    a=1

# note : this has been made in summer 2024, the game may have had some extensions since then ( if yes, add "extension" column )
def allCards(writeAllInFile=False):
    cards = []
    for i in range(1, 270):
        cards.append(singleCard("https://oathcards.seiyria.com/card/OATH-" + get3digitFormat(i) + "?q=&d=images&s=name&b=asc&p=0"))
    df = pd.DataFrame(cards, columns=['Title', 'Category', 'Type', 'Effect', 'FAQ text', 'image', 'site_capacity'])
    
    if writeAllInFile:
        df.to_csv("AllCards.csv", index=False)
        
    return df

def singleCard(url, writeInFile=False):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    data = []
    
    # ----------------    Categories    ----------------
    chips = [chip.get_text(strip=True) for label in soup.findAll('ion-label') for chip in label.find_all('ion-chip')]
    extension = chips[0]
    category = chips[1] if len(chips) > 1 else 'Victory condition' if extension == 'Reference' else None
    # TODO : find some program thing to recognize if there is a tree, advisor or nothing to get better type recognition
    type = chips[2] if len(chips) > 2 else None
    
    # ---------------- Main cards features ----------------
    title = soup.find('h1').get_text()
    image = 'https://ledercardcdn.seiyria.com/cards/oath/en-US/' + text_to_image_link(title) + '.webp'
    effect = get_content(soup.find('app-card-text').find('p'))
    
    site_capacity = next((int(p.text.split(":")[1]) for p in soup.find_all('p') if "Card Capacity" in p.text), None)
    
    # ---------------- FAQ and More Oath ----------------
    ion_items = soup.find_all('ion-item', itemtype="https://schema.org/Question")
    faq = []
    for item in ion_items:
        question = item.find('h3', itemprop='name').get_text(strip=True)
        answer = item.find('p', itemprop='text').get_text(strip=True)
        faq.append({'question': question, 'answer': answer})
    
    data = [title, category, type, effect, faq, image, site_capacity]
    
    # create simple web page layout for the cards 
    if writeInFile:
        f = open(title + ".html", "w")
        f.write(make_web_page(data))
        
    return data

allCards(True)