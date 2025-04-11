from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

def all() : 
    url = "https://dnd5e.wikidot.com"
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')

    # find feats in page
    feats = soup.find('h1', id='toc70').find_parents()[2].findAll('a')
    
    # get name and link of feat
    allFeats = []
    for feat in feats :
        name = feat.text.strip()
        link = f"https://dnd5e.wikidot.com{feat['href']}"
        allFeats.append({
            'index': len(allFeats),
            'name' : name,
            'link' : link,
        })

    return allFeats

# creates a csv with every feat and its description and possible prerequisites
def complete() :
    complete_feat_list = []
    for feat in all() :
        source = '' 
        prerequisite = ''
        description = []
        boni = []
        main_content = bs(requests.get(feat['link']).content, 'html.parser').find('div', id='page-content')
        for txt in main_content.findAll('p'):
            txt = txt.text.strip()
            if 'Source' in txt : source = txt[7:]
            if 'Prerequisite:' in txt : prerequisite = txt[12:]
            else :
                description.append(txt)

        for li in main_content.findAll('li'):
            boni.append(li.text.strip())
        
        complete_feat_list.append({
            'index': feat['index'],
            'name': feat['name'],
            'link': feat['link'],
            'Source': source if source != '' else None,
            'Description': '. '.join(description),
            'Boni': boni,
            'Prerequisite' : prerequisite if prerequisite != '' else None
        })

    df = pd.DataFrame(complete_feat_list)
    df.to_csv('all_feats.csv', index=False)

    print('Created \'all_feats.csv\'')

    return complete_feat_list


    
    return complete_feat_list




def byName(name) :
    for feat in all() :
        if feat['name'].lower() == name.lower() : return feat
    return -1

def byId(id) : 
    return all()[id]

complete()
