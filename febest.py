import sys
import random
import string
import datetime
import traceback

import pymysql

import setproctitle as spt

import requests
from bs4 import BeautifulSoup

from app.models import ScraperCategory

import scrapers_config as cfg


spt.setproctitle("febest")
sys.stdout = open("logs_febest.log", "w")
sys.stderr = open("logs_febest.log", "w")


def get_current_time():
    return datetime.datetime.now()


def get_categories_from_db():
    cat_query = ScraperCategory.query.filter_by(shop="febest").all()
    cat_dicts = []
    for cq in cat_query:
        cat_dicts.append(dict(cat=cq.cat_link, cat_id=cq.cat_id))
    return cat_dicts


def get_cat_products():
    page_num = 1

    product_links = []

    while True:
        prod_before = len(product_links)

        url = f'{category["cat"]}?p={str(page_num)}'
        html = requests.get(url).text
        bs = BeautifulSoup(html, "html.parser")

        item_divs = bs.find_all("div", {"class": "item-inner"})
        for item_div in item_divs:
            product_link = item_div.find(
                "div", {"class": "products clearfix"}
            ).find("a").attrs["href"]
            if product_link not in product_links:
                product_links.append(product_link)

        prod_after = len(product_links)

        if prod_before == prod_after:
            print("Breaking", flush=True)
            break

        page_num = page_num + 1

    return product_links


def get_product_data():
    def available():
        availability_p = bs.find("p", {"class": "availability"})
        if "In stock" in availability_p.get_text():
            return True
        else:
            return False

    def generate_product_ref():
        def get_ref_codes_from_db():
            ref_connection = pymysql.connect(
                host=cfg.db_data["host"],
                user=cfg.db_data["user"],
                password=cfg.db_data["password"],
                db=cfg.db_data["db"],
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor,
            )
            with ref_connection.cursor() as ref_cursor:
                select_query = "SELECT product_ref FROM parsed_products;"
                ref_cursor.execute(select_query)
                db_data = ref_cursor.fetchall()
            ref_connection.close()

            fetched_refs = []

            for ref_dict in db_data:
                if ref_dict["product_ref"] not in fetched_refs:
                    fetched_refs.append(ref_dict["product_ref"])

            return sorted(fetched_refs)

        def ref_in_list(lst, item):
            low = 0
            high = len(lst) - 1

            while low <= high:
                mid = (low + high) // 2
                guess = lst[mid]
                if guess == item:
                    return True
                if guess > item:
                    high = mid - 1
                else:
                    low = mid + 1
            return False

        def generate():
            digits = string.digits

            char_num = 1
            ref_code = "".join(random.choice(digits) for __ in range(char_num))
            while ref_in_list(existing_codes, int(ref_code)) is True:
                char_num = char_num + 1
                ref_code = "".join(random.choice(digits) for __ in range(char_num))

            return int(ref_code)

        existing_codes = get_ref_codes_from_db()
        value = generate()

        return value

    def get_name():
        return bs.find("h1").get_text()

    def get_art():
        art_div = bs.find("div", {"class": "articulbox"}).get_text()
        return art_div.replace("Code: ", "").strip()

    def get_price():
        price_span = bs.find(
            "span", {"class": "regular-price"}
        ).find("span", {"class": "price"})
        return float(price_span.get_text().replace("€", ""))

    def get_pictures():
        images = []
        pictures_div = bs.find("div", {"class": "more-views"})
        for li in pictures_div.find_all("li"):
            pr_img = li.find("a").attrs["href"]
            if pr_img not in images:
                images.append(pr_img)

        return images

    def get_cars():
        cars_list = []
        compatibility_ul = bs.find("ul", {"class": "compatibility"})
        for li in compatibility_ul.find_all("li"):
            if li.get_text() not in cars_list:
                cars_list.append(li.get_text())
        return ";".join(cars_list)

    def get_weight():
        weight_th = bs.find("th", text="Weight")
        return weight_th.find_next_sibling("td").get_text()

    url = product
    html = requests.get(url).text
    bs = BeautifulSoup(html, "html.parser")

    prods = []

    if available() is True:
        ref = generate_product_ref()
        name = get_name()
        art = get_art()
        price = get_price()
        pictures = get_pictures()
        description = get_cars()
        weight = get_weight()

        results_dict = dict(
            url=url,
            cat_id=cat_id,
            ref=ref,
            color=None,
            name=name,
            art=art,
            price=price,
            pictures=pictures,
            description=description,
            sizes=None,
            materials=None,
            weight=weight
        )

        prods.append(results_dict)

        connection = pymysql.connect(
            host=cfg.db_data["host"],
            user=cfg.db_data["user"],
            password=cfg.db_data["password"],
            db=cfg.db_data["db"],
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

        try:
            print(results_dict["name"], flush=True)
            ts = datetime.datetime.now()

            shop_id = 6
            url = results_dict["url"]
            product_ref = results_dict["ref"]
            parsed = ts
            updated = ts
            name = results_dict["name"]
            available = 1
            brand = "febest"
            art = results_dict["art"]
            current_price = results_dict["price"]
            currency = "EUR"
            description = results_dict["description"]
            material = results_dict["materials"]
            dimensions = str(results_dict["sizes"])
            images = ", ".join(results_dict["pictures"])
            img_main = results_dict["pictures"][0]
            img_additional = ", ".join(results_dict["pictures"])
            category_id = results_dict["cat_id"]
            color = results_dict["color"]
            weight = int(float(results_dict["weight"]) * 1000)

            with connection.cursor() as cursor:
                insert_query = "INSERT INTO parsed_products_test (" \
                                "shop_id, url, product_ref, parsed, updated, name," \
                                " available, brand, art, current_price, currency," \
                                " description, material, dimensions," \
                                " images, img_main, img_additional, category, " \
                                "color, weight)" \
                                " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                                " %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                insert_values = (
                    shop_id, url, product_ref, parsed, updated, name, available,
                    brand, art, current_price, currency, description, material,
                    dimensions, images, img_main, img_additional, category_id,
                    color, weight
                )
                cursor.execute(insert_query, insert_values)

                connection.commit()
        except IndexError:
            pass

        connection.close()

    else:
        print(get_current_time(), "The item is out of stock.")

    print("--- --- ---")

    return prods


def write_db():
    connection = pymysql.connect(
        host=cfg.db_data["host"],
        user=cfg.db_data["user"],
        password=cfg.db_data["password"],
        db=cfg.db_data["db"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )

    for result in results:
        try:
            print(result["name"], flush=True)
            ts = datetime.datetime.now()

            shop_id = 6
            url = result["url"]
            product_ref = result["ref"]
            parsed = ts
            updated = ts
            name = result["name"]
            available = 1
            brand = "febest"
            art = result["art"]
            current_price = result["price"]
            currency = "EUR"
            description = result["description"]
            material = result["materials"]
            dimensions = str(result["sizes"])
            images = ", ".join(result["pictures"])
            img_main = result["pictures"][0]
            img_additional = ", ".join(result["pictures"])
            category_id = result["cat_id"]
            color = result["color"]
            weight = int(float(result["weight"]) * 1000)

            with connection.cursor() as cursor:
                insert_query = "INSERT INTO parsed_products_test (" \
                               "shop_id, url, product_ref, parsed, updated, name," \
                               " available, brand, art, current_price, currency," \
                               " description, material, dimensions," \
                               " images, img_main, img_additional, category, " \
                               "color, weight)" \
                               " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                               " %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                insert_values = (
                    shop_id, url, product_ref, parsed, updated, name, available,
                    brand, art, current_price, currency, description, material,
                    dimensions, images, img_main, img_additional, category_id,
                    color, weight
                )
                cursor.execute(insert_query, insert_values)

                connection.commit()
        except IndexError:
            pass

    connection.close()


if __name__ == "__main__":
    categories = get_categories_from_db()

    for category in categories:
        cat_id = category["cat_id"]
        print(
            get_current_time(), f"Gathering products in {category['cat']}", flush=True
        )
        products = get_cat_products()
        print(get_current_time(), "Done!", flush=True)
        for product in products:
            try:
                print("Gathering data:", product, flush=True)
                get_product_data()
            except Exception:
                traceback.print_exc()

        print("--- --- ---", flush=True)
