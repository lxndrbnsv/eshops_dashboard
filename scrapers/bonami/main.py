import sys
import re
import json
import random
import string
import datetime
import traceback

import requests
from bs4 import BeautifulSoup
from write_db import WriteProducts


sys.stdout = open("logs.log", "w")
sys.stderr = open("logs.log", "w")


def read_categories():
    with open("categories.json", "r") as json_file:
        json_data = json.load(json_file)

    return json_data


def get_product_list():
    product_list = []

    page_num = 0

    while True:
        page = f"{cat_url}?p={str(page_num)}"
        print(page)
        print(len(product_list))
        cat_html = requests.get(page).text
        cat_bs = BeautifulSoup(cat_html, "html.parser")

        old_len = len(product_list)
        for a in cat_bs.find_all("a"):
            try:
                if ".cz/p/" in a.attrs["href"]:
                    if a.attrs["href"] not in product_list:
                        product_list.append(a.attrs["href"])
            except KeyError:
                pass
        new_len = len(product_list)

        if old_len == new_len:
            break
        page_num = page_num + 1

    return product_list


def get_name():
    return bs.find("h1").get_text().strip()


def get_art():
    art_header = bs.find("h4", text="Číslo produktu")
    return art_header.find_next_sibling("p").get_text().strip()


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


def get_price():
    old_price_span = bs.find("span", {"class": "s3pgx0af1"})
    old_price = old_price_span.get_text().replace("Kč", "").strip()

    try:
        new_price = (
            old_price_span.find_next_sibling("span")
            .get_text()
            .replace("Kč", "")
            .strip()
        )

    except AttributeError:
        new_price = "0"
    except TypeError:
        new_price = "0"

    int_1 = int(re.sub("\D", "", old_price))
    int_2 = int(re.sub("\D", "", new_price))

    old = max(int_1, int_2)
    new = min(int_1, int_2)

    price_dict = dict(
        old_price=str(old),
        new_price=str(new),
    )

    return price_dict


def get_dimensions():
    dims_header = bs.find("h4", text="Rozměry")
    try:
        return (
            dims_header.find_next_sibling("p")
            .get_text()
            .strip()
            .split(" cm", 1)[0]
        )
    except AttributeError:
        return None


def get_length():
    length_header = bs.find("h4", text="Délka")
    try:
        return int(
            length_header.find_next_sibling("p")
            .get_text()
            .strip()
            .split(" cm", 1)[0]
            .split(".", 1)[0]
            .split(",", 1)[0]
            .strip()
        )
    except AttributeError:
        pass
    except TypeError:
        pass
    try:
        if dimensions is not None:
            return int(
                dimensions.split(" x", 1)[0].split(".", 1)[0].split(",", 1)[0]
            )
        else:
            return 2
    except IndexError:
        print("IE")
        return 2
    except ValueError:
        print("VE")
        return 2


def get_height():
    height_header = bs.find("h4", text="Výška")
    try:
        return int(
            height_header.find_next_sibling("p")
            .get_text()
            .strip()
            .split(" cm", 1)[0]
            .split(".", 1)[0]
            .split(",", 1)[0]
            .strip()
        )
    except AttributeError:
        pass
    except TypeError:
        pass

    try:
        if dimensions is not None:
            return int(
                dimensions.split("x ", 1)[1]
                .strip()
                .split(" ", 1)[0]
                .split(".", 1)[0]
                .split(",", 1)[0]
            )
        else:
            return 0
    except IndexError:
        print("IE")
        return 2
    except ValueError:
        print("VE")
        return 2


def get_width():
    width_header = bs.find("h4", text="Šířka")
    try:
        return int(
            width_header.find_next_sibling("p")
            .get_text()
            .strip()
            .split(".", 1)[0]
            .split(",", 1)[0]
            .split(" cm", 1)[0]
            .strip()
        )
    except AttributeError:
        pass
    except TypeError:
        pass
    try:
        if dimensions is not None:
            return int(
                dimensions.rsplit("x ", 1)[1]
                .split(" cm", 1)[0]
                .split(".", 1)[0]
                .split(",", 1)[0]
            )
        else:
            return 2
    except IndexError:
        print("IE")
        return 2
    except ValueError:
        print("VE")
        return 2


def get_diameter():
    try:
        diameter_header = bs.find("h4", text="Průměr")
        return (
            diameter_header.find_next_sibling("p")
            .get_text()
            .strip()
            .replace(".", ",")
            .replace(" cm", "")
        )
    except AttributeError:
        return None


def get_description():
    description_div = bs.find("div", {"class": "s813pxiav"})
    if description_div is not None:
        return description_div.get_text().strip()
    else:
        return None


def get_pictures():
    pics = []
    pictures_div = bs.find("div", {"class": "scc1150ew"})

    pics.append(
        pictures_div.find("picture")
        .find("source")
        .attrs["srcset"]
        .split(" ", 1)[0]
    )

    return pics


def get_weight():
    try:
        weight_header = bs.find("h4", text="Hmotnost")
        return (
            weight_header.find_next_sibling("p")
            .get_text()
            .strip()
            .replace(".", ",")
            .split(" ", 1)[0]
        )
    except AttributeError:
        return None


def get_material():
    try:
        material_header = bs.find("h4", text="Materiál")
        return material_header.find_next_sibling("p").get_text().strip()
    except AttributeError:
        return None


def if_available():
    available_span = bs.find("span", {"class": "s74wkbceb"})
    if "Skladem" in available_span.get_text():
        return 1
    else:
        return 0


def get_variants():
    variants_list = []
    variants_div = bs.find("div", {"class": "s9xuijxfi"})
    if variants_div is None:
        return []
    else:
        for a in variants_div.find_all("a"):
            try:
                if a.attrs["href"] not in variants_list:
                    variants_list.append(a.attrs["href"])
            except KeyError:
                pass
        return variants_list


if __name__ == "__main__":
    viewed_products = []  # Список просмотренных продуктов.
    cat_data = read_categories()
    results = []
    for cat_dict in cat_data[2:]:
        cat_url = cat_dict["cat"]
        products = get_product_list()
        for product in products:
            try:
                if product not in viewed_products:
                    html = requests.get(product).text
                    bs = BeautifulSoup(html, "html.parser")

                    variants = get_variants()
                    if len(variants) == 0:

                        cat_id = cat_dict["cat_id"]
                        url = cat_url
                        name = get_name()
                        art = get_art()
                        product_ref = generate_product_ref()
                        price = get_price()
                        if price["new_price"] != "0":
                            new_price = price["new_price"]
                            old_price = price["old_price"]
                        else:
                            price = price["old_price"]
                            new_price = price
                            old_price = None
                        dimensions = get_dimensions()
                        length = get_length()
                        height = get_height()
                        width = get_width()
                        diameter = get_diameter()
                        weight = get_weight()
                        material = get_material()
                        description = get_description()
                        pictures = get_pictures()
                        available = if_available()

                        parameters = dict(diameter=diameter, material=material)

                        print(product)

                        result = dict(
                            shop_id="4",
                            available=available,
                            timestamp=round(
                                datetime.datetime.now().timestamp()
                            ),
                            cat_id=cat_dict["cat_id"],
                            url=product,
                            name=name,
                            art=art,
                            product_ref=product_ref,
                            price=price,
                            currency="CZK",
                            description=description,
                            parameters=parameters,
                            height=height,
                            length=length,
                            width=width,
                            dimensions=dimensions,
                            pictures=pictures,
                            img_main=pictures[0],
                            img_additional=pictures,
                            img_main_url=f"http://3.127.139.108/api/images/4/{product_ref}.jpg",
                            img_additional_url=None,
                            language="CZ",
                            additional_attrs=None,
                            power_consumption=None,
                            weight=weight,
                            old_price=old_price,
                            discount=None,
                            color=None,
                        )

                        results.append(result)
                    else:
                        for variant in variants:
                            variant = product
                            html = requests.get(variant).text
                            bs = BeautifulSoup(html, "html.parser")

                            cat_id = cat_dict["cat_id"]
                            url = cat_url
                            name = get_name()
                            art = get_art()
                            product_ref = generate_product_ref()
                            price = get_price()
                            if price["new_price"] != "0":
                                new_price = price["new_price"]
                                old_price = price["old_price"]
                            else:
                                price = price["old_price"]
                                new_price = price
                                old_price = None
                            dimensions = get_dimensions()
                            length = get_length()
                            height = get_height()
                            width = get_width()
                            diameter = get_diameter()
                            weight = get_weight()
                            material = get_material()
                            description = get_description()
                            pictures = get_pictures()
                            available = if_available()

                            parameters = dict(
                                diameter=diameter, material=material
                            )

                            print(product)

                            result = dict(
                                shop_id="4",
                                available=available,
                                timestamp=round(
                                    datetime.datetime.now().timestamp()
                                ),
                                cat_id=cat_dict["cat_id"],
                                url=product,
                                name=name,
                                art=art,
                                product_ref=product_ref,
                                price=price,
                                currency="CZK",
                                description=description,
                                parameters=parameters,
                                height=height,
                                length=length,
                                width=width,
                                dimensions=dimensions,
                                pictures=pictures,
                                img_main=pictures[0],
                                img_additional=pictures,
                                img_main_url=f"http://3.127.139.108/api/images/3/{product_ref}.jpg",
                                img_additional_url=None,
                                language="CZ",
                                additional_attrs=None,
                                power_consumption=None,
                                weight=weight,
                                old_price=old_price,
                                discount=None,
                                color=None,
                            )

                            results.append(result)

                            viewed_products.append(product)
            except Exception as error:
                traceback.print_exc()
    WriteProducts(results)
