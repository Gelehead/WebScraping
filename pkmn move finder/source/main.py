import allMoveSearch
import getMon
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Parameter 
#   every pokemon move as a list
# 
# Returns
#   [selectedMove, -1 if not selected any]
def askForMove(listOfMoves):
    searchedMove = input(print("Enter a part of the pokemon move you are searching: "))
    possibleResults = []
    for elem in listOfMoves:
        elem = elem.lower()
        if elem.find(searchedMove) != -1:
            possibleResults.append(elem)
            
    print(pd.DataFrame(possibleResults, columns=['Move Name']))
    answer = int(input("\nChoose the number corresponding to the move you search \n   IF YOU MADE AN ERROR, ENTER -1: \n"))
    
    return [possibleResults[answer] if answer != -1 else None, answer]


def main():
    moveNames = allMoveSearch.get(True)['Name'].tolist()
    
    # SEARCH LOOP
    searchedMoves = []
    done = False
    while done == False: 
    
        # USER INPUT
        answer = ["MOVE NAME HERE", -1]
        while answer[1] == -1:
            answer = askForMove(moveNames)
        searchedMoves.append(answer[0])
    
        print()
        print(searchedMoves)
        print()
        done = input(print("Another move? \n [y/yes] [n/no]")) != ("y" or "yes")
        
        
    # GET MATCHING MONS
    pkList = []
    for move in searchedMoves: 
        pkList.append(getMon.byMove(move))
        
    result = set(pkList[0])
    for s in pkList[1:]:
        result.intersection_update(s)
    print(result if result != set() else "No pokemon have those moves in common")
    
    return result
    
        
main()