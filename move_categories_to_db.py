import json

from app import db
from app.models import ScraperCategory

# TODO:  удалить все категории, у которых нет соответствия.
# TODO:  брать категории для парсинга прямо из БД.
while True:
    shop_name = input("Shop name: ")

    file_path = f"./scrapers/{shop_name}/categories.json"

    try:
        with open(file_path, "r") as json_file:
            json_data = json.load(json_file)

        for d in json_data:
            scraper_cat = ScraperCategory()
            scraper_cat.cat_link = d["cat"]
            scraper_cat.cat_id = int(d["cat_id"])
            scraper_cat.shop = shop_name
            db.session.add(scraper_cat)
        db.session.commit()

        print(f"Added {shop_name} to DB.")

        while True:
            if_continue = input("1 - add another categories    2 - quit\n")
            if if_continue == "1":
                break
            elif if_continue == "2":
                print("Exiting...")
                quit()
                break
            else:
                print("Please select 1 or 2!")

    except FileNotFoundError:
        print("No such file!")
