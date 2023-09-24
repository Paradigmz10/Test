import requests
from bs4 import BeautifulSoup
import pickle
import os
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)

CACHE_FILE = 'cache.pkl'
CACHE_EXPIRATION = timedelta(days=1)

def fetch_continent_mapping():
    url = "https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_by_continent_(data_file)"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    trs = soup.find_all("table")[2].find("tbody").find_all("tr")[1:]
    cc = {}
    for tr in trs:
        tds = tr.find_all("td")
        cc[tds[1].text] = tds[0].text
    return cc

def fetch_country_codes(continent_mapping):
    url = "https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    trs = soup.find("table").find("tbody").find_all("tr")[2:]
    countries = []
    for tr in trs:
        tds = tr.find_all("td")
        if len(tds) == 1:
            continue
        name = tds[0].find_all("a")[1].text
        iso_alpha_2 = tds[3].find("span").text
        iso_alpha_3 = tds[4].find("span").text
        iso_numeric = tds[5].find("span").text
        continent = continent_mapping.get(iso_alpha_2, "Unknown")
        countries.append((name, iso_alpha_2, iso_alpha_3, iso_numeric, continent))
    return countries

def cache_data(data):
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump((datetime.now(), data), f)

def load_cached_data():
    if not os.path.exists(CACHE_FILE):
        return None
    with open(CACHE_FILE, 'rb') as f:
        timestamp, data = pickle.load(f)
        if datetime.now() - timestamp < CACHE_EXPIRATION:
            return data
    return None

def main():
    countries = load_cached_data()
    if not countries:
        logging.info("Fetching data from Wikipedia...")
        continent_mapping = fetch_continent_mapping()
        countries = fetch_country_codes(continent_mapping)
        cache_data(countries)
    else:
        logging.info("Loading data from cache...")
    
    continent_filter = input("Enter continent name to filter (leave empty for all): ").capitalize()
    filtered_countries = [country for country in countries if continent_filter in country[4]]
    
    print("Countries:")
    for country in filtered_countries:
        print(f'("{country[0]}", "{country[1]}", "{country[2]}", "{country[3]}", "{country[4]}")')

if __name__ == "__main__":
    main()
