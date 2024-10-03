import requests
from bs4 import BeautifulSoup
import pandas as pd

def byMove(move):
    move.replace(",", "")
    move.replace("'", "")
    url = "https://pokemondb.net/move/" + move.replace(" ","-")
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    pkmns = []
    for card in soup.find_all('div', class_="infocard"):
        pkName = card.find('span', class_='infocard-md-data').find('a').get_text()
        pkmns.append(pkName) if pkName not in pkmns else None

    df = pd.DataFrame(pkmns, columns=['Name'])
    
    df.to_csv(move + ".csv", index=False)
    
    return df['Name'].tolist()
        