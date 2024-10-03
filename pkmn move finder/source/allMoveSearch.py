import requests
from bs4 import BeautifulSoup
import pandas as pd

# Utility functions 
def getFromLastOccurence(string, character):
    return string[string.rfind(character)+1:]


# try here to write documentation you can see when hovering the function in different files
def get(writeInFile=False):
    """ with beautifulSoup, pandas and requests, get all pokemon moves from pokemondb.net

    Args:
        writeInFile (bool, optional): True creates a file named AllMoves.csv with all pokemon moves. Defaults to False.

    Returns:
        _type_: csv file with all pkmns moves
    """
    url = "https://pokemondb.net/move/all"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    moves = []
    for cell in soup.find('table').find('tbody').select('tr'):
        moveName = cell.find('td', class_='cell-name').find('a', class_='ent-name').get_text()
        moveType = cell.find('td', class_='cell-icon').find('a').get_text()
        moveCat = cell.find('td', class_='cell-icon text-center')['data-sort-value']
        movePower_Acc_PP_ProbofsecEffect = []
        for cellNum in cell.select('td.cell-num'):
            movePower_Acc_PP_ProbofsecEffect.append(cellNum.get_text())
        moveEff = cell.find('td', class_='cell-long-text')
        moves.append([moveName, moveType, moveCat,\
                      '-' if movePower_Acc_PP_ProbofsecEffect[0] == '—' else movePower_Acc_PP_ProbofsecEffect[0], \
                      '-' if movePower_Acc_PP_ProbofsecEffect[1] == '—' else movePower_Acc_PP_ProbofsecEffect[1], \
                      '-' if movePower_Acc_PP_ProbofsecEffect[2] == '—' else movePower_Acc_PP_ProbofsecEffect[3], \
                      moveEff, \
                      '-' if movePower_Acc_PP_ProbofsecEffect[3] == '—' else movePower_Acc_PP_ProbofsecEffect[3]])

    # did not get what the dataFrame is for
    df = pd.DataFrame(moves, columns=['Name', 'Type', 'Category', 'Power', 'Accuracy', 'PP', 'Effect', 'Prob of effect'])

    if writeInFile:
        df.to_csv("AllMoves.csv", index=False)
        
    return df