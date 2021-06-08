import sys
import json
import string
import random
import datetime

import requests
from bs4 import BeautifulSoup

from write_db import WriteProducts


sys.stdout = open("logs.log", "w")
sys.stderr = open("logs.log", "w")


def generate_product_ref():
    def generate():
        digits = string.digits
        try:
            with open("./ref_codes.txt", "r") as txt_file:
                text_data = txt_file.readlines()

            existing_codes = []
            for t in text_data:
                existing_codes.append(t.replace("\n", ""))
        except FileNotFoundError:
            existing_codes = []

        char_num = 1
        ref_code = "".join(random.choice(digits) for __ in range(char_num))
        while ref_code in existing_codes:
            char_num = char_num + 1
            ref_code = "".join(random.choice(digits) for __ in range(char_num))

        return int(ref_code)

    value = generate()
    with open("./ref_codes.txt", "a+") as text_file:
        text_file.write(f"{value}\n")

    return value


def get_product_links():
    product_links = []

    cat_url = category["cat"]
    cat_html = requests.get(cat_url).text
    cat_bs = BeautifulSoup(cat_html, "html.parser")

    for i in cat_bs.find_all("div", {"class": "product-list-item"}):
        prod = "https://eshop.tescoma.cz" + i.find("a").attrs["href"]
        if prod not in product_links:
            product_links.append(prod)

    pagination_area = cat_bs.find("nav", {"class": "pagination"})
    if pagination_area is not None:
        for a in pagination_area.find_all("a", {"class": "pagination-link"}):
            page_url = f"https://eshop.tescoma.cz{a.attrs['href']}"
            page_html = requests.get(page_url).text
            page_bs = BeautifulSoup(page_html, "html.parser")

            for i in page_bs.find_all("div", {"class": "product-list-item"}):
                prod = "https://eshop.tescoma.cz" + i.find("a").attrs["href"]
                if prod not in product_links:
                    product_links.append(prod)

    return product_links


def get_name():
    return bs.find("h1", {"class": "title"}).get_text().strip()


def get_description():
    return bs.find("div", {"id": "description"}).get_text().strip()


def get_price():
    price_tag = bs.find("div", {"class": "product-price"})
    return (
        price_tag.find("div", {"class": "price"})
        .find("span", {"class": "value"})
        .get_text()
        .replace("Kč", "")
        .strip()
    )


def get_discount():
    price_tag = bs.find("div", {"class": "product-price"})
    discount_tag = price_tag.find(
        "div", {"class": "product-reduction-percent"}
    )

    if discount_tag is not None:
        return discount_tag.find("span", {"class": "value"}).get_text().strip()
    else:
        return None


def get_old_price():
    try:
        old_price_tag = bs.find("span", text="Původní cena vč. DPH:")
        old_price = (
            old_price_tag.find_next_sibling("span")
            .get_text()
            .replace("Kč", "")
            .strip()
        )
    except AttributeError:
        old_price = None

    return old_price


def get_art():
    return bs.find("span", {"class": "product-code"}).get_text().strip()


def if_available():
    available = bs.find("div", {"class": "availability"}).get_text().strip()
    if available == "skladem v eshopu":
        return 1
    else:
        return 0


def get_diameter():
    try:
        for strong in bs.find_all("strong", {"class": "parameter-label"}):
            if "Průměr" in strong.get_text():
                return (
                    strong.find_next_sibling("span")
                    .find("span")
                    .get_text()
                    .strip()
                )
    except AttributeError:
        return None


def get_dishwasher():
    try:
        for strong in bs.find_all("strong", {"class": "parameter-label"}):
            if "Mytí v myčce" in strong.get_text():
                return (
                    strong.find_next_sibling("span")
                    .find("span")
                    .get_text()
                    .strip()
                )
    except AttributeError:
        return None


def get_oven():
    try:
        for strong in bs.find_all("strong", {"class": "parameter-label"}):
            if "Vhodné do trouby" in strong.get_text():
                return (
                    strong.find_next_sibling("span")
                    .find("span")
                    .get_text()
                    .strip()
                )
    except AttributeError:
        return None


def get_material():
    try:
        for strong in bs.find_all("strong", {"class": "parameter-label"}):
            if "Materiál" in strong.get_text():
                return (
                    strong.find_next_sibling("span")
                    .find("span")
                    .get_text()
                    .strip()
                )
    except AttributeError:
        return None


def get_volume():
    try:
        for strong in bs.find_all("strong", {"class": "parameter-label"}):
            if "Objem" in strong.get_text():
                return (
                    strong.find_next_sibling("span")
                    .find("span")
                    .get_text()
                    .strip()
                )
    except AttributeError:
        return None


def get_power_consumption():
    try:
        for strong in bs.find_all("strong", {"class": "parameter-label"}):
            if "Příkon" in strong.get_text():
                return (
                    strong.find_next_sibling("span")
                    .find("span")
                    .get_text()
                    .strip()
                )
    except AttributeError:
        return None


def get_height():
    try:
        for strong in bs.find_all("strong", {"class": "parameter-label"}):
            if "Výška" in strong.get_text():
                return (
                    strong.find_next_sibling("span")
                    .find("span")
                    .get_text()
                    .strip()
                )
    except AttributeError:
        return None


def get_length():
    try:
        for strong in bs.find_all("strong", {"class": "parameter-label"}):
            if "Délka" in strong.get_text():
                return (
                    strong.find_next_sibling("span")
                    .find("span")
                    .get_text()
                    .strip()
                )
    except AttributeError:
        return None


def get_width():
    try:
        for strong in bs.find_all("strong", {"class": "parameter-label"}):
            if "Šířka" in strong.get_text():
                return (
                    strong.find_next_sibling("span")
                    .find("span")
                    .get_text()
                    .strip()
                )
    except AttributeError:
        return None


def get_weight():
    try:
        for strong in bs.find_all("strong", {"class": "parameter-label"}):
            if "Hmotnost" in strong.get_text():
                return (
                    strong.find_next_sibling("span")
                    .find("span")
                    .get_text()
                    .strip()
                )
    except AttributeError:
        return None


def get_fridge():
    try:
        for strong in bs.find_all("strong", {"class": "parameter-label"}):
            if "Vhodné do lednice" in strong.get_text():
                return (
                    strong.find_next_sibling("span")
                    .find("span")
                    .get_text()
                    .strip()
                )
    except AttributeError:
        return None


def get_slip():
    try:
        for strong in bs.find_all("strong", {"class": "parameter-label"}):
            if "Protiskluzová úprava" in strong.get_text():
                return (
                    strong.find_next_sibling("span")
                    .find("span")
                    .get_text()
                    .strip()
                )
    except AttributeError:
        return None


def get_quantity():
    try:
        for strong in bs.find_all("strong", {"class": "parameter-label"}):
            if "Počet ks v sadě" in strong.get_text():
                return (
                    strong.find_next_sibling("span")
                    .find("span")
                    .get_text()
                    .strip()
                )
    except AttributeError:
        return None


def get_pics():
    pic_links = []

    for pic in bs.find_all("picture"):
        try:
            source = pic.find("source").attrs["data-lazy-srcset"]
            if source not in pic_links and "preview" not in source:
                pic_links.append(source)
        except KeyError:
            pass

    pic_names = []

    for pic in pic_links:
        image_name = pic.rsplit("/", 1)[1].split(".", 1)[0]
        r = requests.get(pic, allow_redirects=True)
        open(f"./files/pics/{shop_id}/{image_name}.jpg", "wb").write(r.content)
        pic_names.append(f"{image_name}.jpg")

    pics = []

    for pic in pic_names:
        pics.append(f"http://3.127.139.108/api/images/{shop_id}/{pic}.jpg")

    return {"pics_all": pics, "pic_names": pic_names}


def get_variations():
    variants = []
    variants_div = bs.find("ul", {"class": "variants"})
    if variants_div is not None:
        for input_tag in variants_div.find_all("input"):
            try:
                if (
                    f"https://eshop.tescoma.cz{input_tag.attrs['data-url']}"
                    not in variants
                ):
                    variants.append(
                        dict(
                            link=f"https://eshop.tescoma.cz{input_tag.attrs['data-url']}",
                            color=input_tag.find_parent("li")
                            .find("img")
                            .attrs["alt"],
                        )
                    )
            except AttributeError:
                pass
    return variants


if __name__ == "__main__":
    results = []
    shop_id = 2
    language = "CZ"
    currency = "CZK"

    with open("./categories.json", "r") as json_file:
        categories = json.load(json_file)

    for category in categories:
        try:
            print(category)

            links = get_product_links()
            for link in links:
                print(link)
                html = requests.get(link).text
                bs = BeautifulSoup(html, "html.parser")

                ref_code = generate_product_ref()
                name = get_name()
                description = get_description()
                price = get_price()
                discount = get_discount()
                art = get_art()
                available = if_available()
                height = get_height()
                length = get_length()
                width = get_width()
                weight = get_weight()
                fridge = get_fridge()
                material = get_material()
                volume = get_volume()
                power_consumption = get_power_consumption()
                dishwasher = get_dishwasher()
                oven = get_oven()
                diameter = get_diameter()
                anti_slip = get_slip()
                pictures = get_pics()
                old_price = get_old_price()
                discount = get_discount()
                quantity = get_quantity()
                variants = get_variations()
                color = None

                if height is None:
                    h = "2"
                else:
                    h = height
                if length is None:
                    l = "2"
                else:
                    l = length
                if width is None:
                    w = "2"
                else:
                    w = width

                dimensions = f"{l}x{h}x{w}"

                if quantity is None:
                    quantity = "1"

                parameters = dict(
                    volume=volume,
                    diameter=diameter,
                    oven=oven,
                    dishwasher=dishwasher,
                    material=material,
                    quantity=quantity,
                    fridge=fridge,
                    anti_slip=anti_slip
                )

                result = dict(
                    shop_id=shop_id,
                    available=available,
                    timestamp=round(datetime.datetime.now().timestamp()),
                    cat_id=category["cat_id"],
                    url=link,
                    name=name,
                    art=art,
                    product_ref=ref_code,
                    price=price,
                    currency=currency,
                    description=description,
                    parameters=parameters,
                    height=height,
                    length=length,
                    width=width,
                    dimensions=dimensions,
                    pictures=pictures,
                    img_main=pictures["pics_all"][0],
                    img_additional=pictures["pics_all"][1:],
                    img_main_url=pictures["pics_all"][0],
                    img_additional_url=pictures["pics_all"][1:],
                    language=language,
                    additional_attrs=None,
                    power_consumption=power_consumption,
                    weight=weight,
                    old_price=old_price,
                    discount=discount,
                    color=color,
                )

                if len(variants) > 0:
                    for variant in variants:
                        link = variant["link"]
                        color = variant["color"]

                        result = dict(
                            shop_id=shop_id,
                            available=available,
                            timestamp=round(
                                datetime.datetime.now().timestamp()
                            ),
                            cat_id=category["cat_id"],
                            url=link,
                            name=name,
                            art=art,
                            product_ref=ref_code,
                            price=price,
                            currency=currency,
                            description=description,
                            parameters=parameters,
                            height=height,
                            length=length,
                            width=width,
                            dimensions=dimensions,
                            pictures=pictures,
                            img_main=pictures["pics_all"][0],
                            img_additional=pictures["pics_all"][1:],
                            img_main_url=pictures["pics_all"][0],
                            img_additional_url=pictures["pics_all"][1:],
                            language=language,
                            additional_attrs=None,
                            power_consumption=power_consumption,
                            weight=weight,
                            old_price=old_price,
                            discount=discount,
                            color=color,
                        )

                        results.append(result)
                else:
                    results.append(result)

        except AttributeError:
            print("AE!")

        print("--- --- ---")
    WriteProducts(results)
