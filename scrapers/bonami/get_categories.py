import json

import requests
from bs4 import BeautifulSoup


categories = []

links = ["https://www.bonami.cz/c/kategorie"]

for link in links:
    print(link)
    url = link
    html = requests.get(link).text
    bs = BeautifulSoup(html, "html.parser")

    page_links = bs.find_all("a")

    temp_links = []

    for page_link in page_links:
        try:
            if (
                "https://www.bonami.cz/c/" in page_link.attrs["href"]
                and page_link.attrs["href"] not in links
                and page_link.attrs["href"] not in temp_links
            ):
                temp_links.append(page_link.attrs["href"])
        except KeyError:
            pass

    for temp_link in temp_links:
        if temp_link not in links:
            links.append(temp_link)

    if len(temp_links) == 0:
        categories.append(link)

    print(len(categories))

print("---")

cat_data = []
for c in categories:
    cat_data.append(dict(cat=c, cat_id=15))

json_data = json.dumps(cat_data)

with open("categories.json", "w+") as json_file:
    json_file.write(json_data)
