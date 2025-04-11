import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# level is a number [0-9] describing the spell level, a cantrip is a lvl 0 spell
def byLevel(level):

    def parse_spell_details(spell_link):
        url = spell_link
        response = requests.get(url)
        soup = bs(response.content, 'html.parser')
        paragraphs = soup.find('div', id="page-content").select('p')[3:]
        
        description = []
        at_higher_levels = None
        spell_lists = None

        for para in paragraphs:
            text = para.text.strip()

            if "At Higher Levels" in text:
                at_higher_levels = text
            elif "Spell Lists" in text:
                spell_lists = [item.strip() for item in text.replace("Spell Lists. ", "").split(",")]
            else:
                description.append(text)

        return [description, at_higher_levels, spell_lists]

    url = "https://dnd5e.wikidot.com/spells"
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')

    spells = [] 
    table = soup.find('div', class_="yui-content").findAll('table', class_="wiki-content-table")[level]
    
    for row in table.findAll('tr')[1:]:
        columns = row.findAll('td')
        
        link_tag = columns[0].find('a')
        spell_name = link_tag.text.strip()
        spell_link = f"https://dnd5e.wikidot.com{link_tag['href']}"

        description, higher_levels, spell_lists = parse_spell_details(spell_link)

        school = columns[1].text.strip()
        cast_time = columns[2].text.strip()
        cast_range = columns[3].text.strip()
        duration = columns[4].text.strip()
        components = columns[5].text.strip()

        # Store the parsed data
        spells.append({
            'level': level,
            'name': spell_name,
            'school': school,
            'cast_time': cast_time,
            'range': cast_range,
            'duration': duration,
            'components': components,
            'description': " ".join(description),
            'at higher levels': higher_levels,
            'spell lists': ", ".join(spell_lists) if spell_lists else None,
        })

    return spells

# Gather all spells across all levels
def gather_all_spells():
    all_spells = []
    for level in range(10):  # Cantrips (0) through level 9 spells
        all_spells.extend(byLevel(level))
    return all_spells

# Fetch all spells and save to CSV
all_spells = gather_all_spells()
df = pd.DataFrame(all_spells)
df.to_csv("all_spells.csv", index=False)

print("CSV containing all spells has been created: all_spells.csv")
