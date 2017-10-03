import json

import requests
from bs4 import BeautifulSoup

r = requests.get("https://news.ycombinator.com")
soup = BeautifulSoup(r.content, "html.parser")

scraps = {}

with open('scraps.json', 'w') as f:
    """ Writing the scrapped data into a json file """

    f.writelines('{')
    index = 0
    for storylink in soup.find_all("a", {"class": "storylink"}):
        scraps['title'] = storylink.string
        scraps['url'] = storylink.get("href")
        json.dump(scraps, f)
        if index != len(soup.find_all("a", {"class": "storylink"})) - 1:
            f.writelines(", ")
        index += 1
    f.writelines('}')
