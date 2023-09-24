import requests
from bs4 import BeautifulSoup

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

def main():
    continent_mapping = fetch_continent_mapping()
    countries = fetch_country_codes(continent_mapping)
    print("countries = (")
    for country in countries:
        print(f'("{country[0]}", "{country[1]}", "{country[2]}", "{country[3]}", "{country[4]}"),')
    print(")")

if __name__ == "__main__":
    main()
