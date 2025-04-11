import pandas as pd
from bs4 import BeautifulSoup, Tag
import requests


def get_all_pkmn(url="https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    data = []

    for 

def get_single_pkmn():
    a=0