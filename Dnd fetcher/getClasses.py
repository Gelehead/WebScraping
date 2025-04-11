from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re

# URLs for D&D classes
classes = {
    "Artificer": "https://dnd5e.wikidot.com/artificer",
    "Barbarian": "https://dnd5e.wikidot.com/barbarian",
    "Bard": "https://dnd5e.wikidot.com/bard",
    "Cleric": "https://dnd5e.wikidot.com/cleric",
    "Druid": "https://dnd5e.wikidot.com/druid",
    "Fighter": "https://dnd5e.wikidot.com/fighter",
    "Monk": "https://dnd5e.wikidot.com/monk",
    "Paladin": "https://dnd5e.wikidot.com/paladin",
    "Ranger": "https://dnd5e.wikidot.com/ranger",
    "Rogue": "https://dnd5e.wikidot.com/rogue",
    "Sorcerer": "https://dnd5e.wikidot.com/sorcerer",
    "Warlock": "https://dnd5e.wikidot.com/warlock",
    "Wizard": "https://dnd5e.wikidot.com/wizard"
}

# Caster-related features to exclude
caster = ['Cantrips (0-Level Spells)', 'Preparing and Casting Spells', 'Spellcasting Ability', 'Ritual Casting']

def clean_text(text):
    """Clean and normalize text by replacing line breaks and special characters."""
    text = text.replace('\n', ' ').strip()
    text = text.replace('‘', "'").replace('’', "'").replace('“', '"').replace('”', '"')
    return re.sub(r'\s+', ' ', text)

def parse_section(section, stop_tags):
    """Parse a section and concatenate text from its siblings until a stopping tag is reached."""
    content = ""
    sibling = section.find_next_sibling()
    while sibling and sibling.name not in stop_tags:
        if sibling.name:  
            content += sibling.get_text(separator=" ", strip=True) + " "
        sibling = sibling.find_next_sibling()
    return clean_text(content)

def getSubclasses(tableSoup):
    TODO = 1

def byName(name):
    """Fetch and parse class data from the URL."""
    url = classes[name]
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')

    # Parse the main table
    table = soup.find('table', class_="wiki-content-table")
    contents = table.findAll('tr')[1].text.strip().split("\n")
    attributes = []

    for row in table.findAll('tr')[2:]:
        columns = row.findAll('td')
        level = {}
        for i in range(len(columns)):
            if contents[i] == "Features":
                level[contents[i]] = columns[i].text.strip().split(", ")
            else:
                level[contents[i]] = re.sub(r'\D', '', columns[i].text.strip()) if columns[i].text.strip() != "-" else 0
        attributes.append(level)

    # Parse additional features
    feats = {}
    classic_feats = {}
    classic_content = soup.find('div', class_='col-lg-12').findAll('h5')
    for section in classic_content[2:]:
        sec_name = section.text.strip()
        if sec_name in caster:
            continue
        classic_feats[sec_name] = parse_section(section, stop_tags={'h5', 'h3'})
    feats['classic feats'] = classic_feats

    class_specific_feats = {}
    class_specific = soup.find('div', class_='col-lg-12').findAll('h3')
    for section in class_specific:
        sec_name = section.text.strip()
        class_specific_feats[sec_name] = parse_section(section, stop_tags={'h3', 'h5'})
    feats['class specific feats'] = class_specific_feats

    subClasses = getSubclasses(soup.findAll('table', class_='wiki-content-table')[-1])

    attributes.append(subClasses)
    attributes.append(feats)

    
    return attributes

# Fetch and process data for all classes
allClasses = {}
for name in classes:
    #print(f"Processing: {name}")
    allClasses[name] = byName(name)

# Convert to DataFrame and save
df = pd.DataFrame(allClasses)
df.to_csv("all_classes.csv", index=False)

