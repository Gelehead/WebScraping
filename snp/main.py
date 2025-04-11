from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import pandas
import requests
import multiprocessing

CHROME_PATH = r'C:\Program Files\Google\Chrome\Application\chrome.exe'


#json object should look like this
""" {
    "company name": {
        "key_data": {
            "exchange": "NYSE", # most likely
            "sector": "industrials",
            "industry": "aerospace",
            "1 year target": "0.00$", #USD
            "today high": "0.00$",
            "today low": "0.00$",
            "today high": "0.00$",
            "share volume": "000,000",
            "average volume": "000,000",
            "previous close": "0.00$",
            "market cap": "000,000,000",
            "forward P/E 1yr": "0.00",
            "Anual dividend": "0.00$",
            "Ex dividend date": "MM/DD/YYYY",
            "Dividend pay date": "MM/DD/YYYY",
            "current yield": "0.0%",
        },
        "common stock": {
            # polynomial description of the function (possibly very large)
            "1 day": [0,1,2,3],
            "1 week": [0,1,2,3],
            "1 month": [0,1,2,3],
            "5 months": [0,1,2,3],
            "1 year": [0,1,2,3],
        }
    }
} """

def printall(arr):
    for a in arr : 
        print(a)

def get_all_pages():
    """
    returns a list of all NYSE snp500 pages from the wikipedia page containing each of them
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    return [[x.text, x['href']] for x in soup.find('table').findAll('a') if "https" in x['href']]

def get_all_infos(name):
    url = "https://www.nasdaq.com/market-activity/stocks/tsla"

    # selenium opening driver, loading page and closing
    options = Options()
    service = Service(CHROME_PATH)

    # Use the correct initialization method
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(url)
    html = driver.find_element("tag name", "html")
    html.send_keys(Keys.END)
    time.sleep(0.1)
    resp = driver.page_source
    driver.quit()

    soup = BeautifulSoup(resp, 'html.parser')
    key_data = get_key_data(soup)
    ## long term we should get 1day / 1week / 1month / 5months 
    return key_data

# get the "key data" from the page 
def get_key_data(soup, driver):
    key_data = {}
    for row in soup.find('div', class_='table-group').findAll('div', class_='table-row'):
        cells = row.find('div')
        if "Today" in cells[0].text :
            key_data["Today's high"] = "".join([c for c in cells[1].text.split('/')[0] if c.isdigit() or c == '.'])
            key_data["Today's low"] = "".join([c for c in cells[1].text.split('/')[1] if c.isdigit() or c == '.'])
        else : 
            key_data[cells[0].text] = cells[1].text

    return key_data

print(get_all_infos("mmm"))


""" for name in get_all_pages()[:15]:
    print("name: ", name)
    print(get_all_infos(name[0])) """

""" if __name__ == '__main__':
    with multiprocessing.Pool() as p : 
        printall(p.map(get_all_infos, get_all_pages())) """