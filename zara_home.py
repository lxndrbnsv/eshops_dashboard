import sys
import json
import string
import random
import traceback
import datetime

from app import db
from app.models import ScraperCategory, RefCode

import setproctitle as spt

import pymysql

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    ElementNotInteractableException,
)

import scrapers_config as cfg


spt.setproctitle("zara_home")
sys.stdout = open("logs_zara_home.log", "w")
sys.stderr = open("logs_zara_home.log", "w")


def get_current_time():
    return datetime.datetime.now()


def fetch_all_ref_codes():
    """Сбор всех существующих реф-кодов из БД."""
    print(get_current_time(), "Fetching ref codes from main database.", flush=True)
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

    ref_codes_list = []

    all_ref_codes = RefCode.query.all()
    for a in all_ref_codes:
        ref_codes_list.append(a.ref_code)
    for f in fetched_refs:
        if f not in ref_codes_list:
            ref_code = RefCode()
            ref_code.ref_code = f
            db.session.add(ref_code)
    db.session.commit()
    print(get_current_time(), "Done", flush=True)


def get_categories_from_db():
    cat_query = ScraperCategory.query.filter_by(shop="zara_home").all()
    cat_dicts = []

    for cq in cat_query:
        cat_dicts.append(dict(cat=cq.cat_link, cat_id=cq.cat_id))

    return cat_dicts


def get_products(cat):
    def accept_cookies():
        try:
            cookie_btn = WebDriverWait(browser, 10).until(
                ec.presence_of_element_located(
                    (By.ID, "onetrust-accept-btn-handler")
                )
            )
            cookie_btn.click()
        except TimeoutException:
            print(
                "Timeout exception while trying to close accept cookies button!",
                flush=True
            )

    def get_links():
        def scroll_to_last_product(product_item):
            print(f"{get_current_time()} Scrolling...", flush=True)
            action.move_to_element(product_item).perform()

        product_links = []

        while True:
            len_in_beginning = len(product_links)

            product_uls = WebDriverWait(browser, 20).until(
                ec.presence_of_all_elements_located((By.CLASS_NAME, "photo-slider"))
            )

            scroll_to_last_product(product_uls[-1])

            for product_ul in product_uls:
                try:
                    link_tag = product_ul.find_element_by_tag_name("a")
                    cat_url = link_tag.get_attribute("href")
                    if cat_url not in product_links:
                        product_links.append(cat_url)
                except NoSuchElementException as no_element:
                    print(no_element, flush=True)
                    pass
            current_len = len(product_links)

            if len_in_beginning == current_len:
                print(
                    f"{get_current_time()} "
                    f"{str(current_len)} products have been collected.",
                    flush=True,
                )
                break

        return product_links

    options = Options()
    options.add_argument(f"--user-agent={cfg.request_data['user_agent']}")
    options.headless = True
    browser = webdriver.Chrome(executable_path=cfg.webdriver["path"], options=options)
    action = ActionChains(browser)
    browser.set_window_size("1366", "768")

    category_url = cat["cat"]
    print(
        f"{get_current_time()} Collecting products in category: {category_url}",
        flush=True,
    )
    product_dicts = []
    try:
        browser.get(category_url)

        accept_cookies()

        links = get_links()

        browser.quit()

        product_dicts = []
        product_links = []  # Список для проверки дубликатов.
        for link in links:
            if link not in product_links:
                product_dicts.append(
                    dict(product_link=link, cat_url=category_url, cat_id=cat["cat_id"])
                )
                product_links.append(link)

        print(f"{get_current_time()} Done!", flush=True)
        print("--- --- ---", flush=True)
    except WebDriverException:
        print("WebDriverException!", flush=True)
        traceback.print_exc()
    except Exception:
        traceback.print_exc()

    return product_dicts


def get_product_data(product_item):
    def close_popups():
        to_close = browser.find_elements_by_class_name("close-dialog")
        for i in to_close:
            try:
                i.click()
            except StaleElementReferenceException:
                pass
            except ElementClickInterceptedException:
                pass
            except ElementNotInteractableException:
                pass

    def generate_product_ref():
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
            generated_code = "".join(random.choice(digits) for __ in range(char_num))
            while ref_in_list(sorted(existing_codes), int(generated_code)) is True:
                char_num = char_num + 1
                generated_code = "".join(
                    random.choice(digits) for __ in range(char_num)
                )

            return int(generated_code)

        existing_codes = []
        for r in RefCode.query.all():
            existing_codes.append(r.ref_code)
        value = generate()

        ref_code = RefCode()
        ref_code.ref_code = value
        db.session.add(ref_code)
        db.session.commit()

        return value

    def colors():
        try:
            WebDriverWait(browser, 5).until(
                ec.presence_of_element_located(
                    (By.CLASS_NAME, "select-color-container")
                )
            )
            return True
        except TimeoutException:
            return False

    def get_current_color():
        color_container = browser.find_element_by_class_name("select-color-container")
        try:
            current_clr = (
                color_container.find_element_by_class_name("on")
                .find_element_by_tag_name("img")
                .get_attribute("title")
            )
        except NoSuchElementException:
            current_clr = None
        return current_clr

    def get_art():
        return browser.find_element_by_class_name("referencia").text.strip()

    def get_name():
        name_div = browser.find_element_by_class_name("header")

        return name_div.find_element_by_tag_name("span").text

    def get_pictures():
        imgs = []
        image_tags = WebDriverWait(browser, 5).until(
            ec.visibility_of_all_elements_located((By.CLASS_NAME, "show-zoom"))
        )
        for image_tag in image_tags:
            imgs.append(image_tag.get_attribute("href"))
        return imgs

    def get_description():
        description_div = browser.find_element_by_id("product-description-paragraphs")
        return description_div.text.strip()

    def get_sizes():
        def sold_out(element):
            if "inactive sold-out" in element.get_attribute("class"):
                return True
            else:
                return False

        def get_size_name(element):
            spans = element.find_elements_by_tag_name("span")
            for span in spans:
                if span.get_attribute("ng-if") == "::size.description":
                    return span.text

        def get_dimensions(element):
            dims = []
            tds = element.find_elements_by_tag_name("td")
            for td in tds:
                if (
                    td.get_attribute("ng-if")
                    == "::itxProductAddToCartSelectorCtrl.showDimensions"
                ):
                    dims.append(td.text.replace("cm", ""))

            if len(dims) > 0:
                return "x".join(dims)
            else:
                spans = element.find_elements_by_tag_name("span")
                for span in spans:
                    if (
                        span.get_attribute("ng-if")
                        == "::(size.displayName && size.description)"
                        or span.get_attribute("ng-if")
                        == "::(size.displayName && !size.description)"
                    ):
                        return span.text

        def get_price(element):
            try:
                price = float(
                    element.find_element_by_class_name("price")
                    .text.replace("€", "")
                    .strip()
                    .replace(",", ".")
                )
                return price
            except NoSuchElementException:
                return float(
                    browser.find_element_by_class_name("price")
                    .text.replace("€", "")
                    .strip()
                    .replace(",", ".")
                )

        sizes_dicts = []

        sizes_parent_tags = browser.find_elements_by_class_name("product-size-row")

        for sizes_parent_tag in sizes_parent_tags:
            if sold_out(sizes_parent_tag) is False:
                size_name = get_size_name(sizes_parent_tag)
                size_dimensions = get_dimensions(sizes_parent_tag)
                size_price = get_price(sizes_parent_tag)

                sizes_dicts.append(
                    dict(
                        size_name=size_name,
                        size_dimensions=size_dimensions,
                        size_price=size_price,
                    )
                )
        return sizes_dicts

    def get_materials():
        info_btn = browser.find_element_by_class_name("button-mas-info")
        try:
            info_btn.click()
        except ElementClickInterceptedException:
            close_popups()
            info_btn.click()

        comps = []

        for i in browser.find_elements_by_class_name("compo"):
            comps.append(i.text)

        close_popups()

        if len(comps) > 0:
            return ", ".join(comps)
        else:
            return None

    options = Options()
    options.add_argument(f"--user-agent={cfg.request_data['user_agent']}")
    options.headless = True
    browser = webdriver.Chrome(executable_path=cfg.webdriver["path"], options=options)
    browser.set_window_size("1920", "1080")

    url = product_item["product_link"]
    cat = product_item["cat_id"]
    print(f"{get_current_time()} Collecting data from {url}", flush=True)
    browser.get(url)

    results = []

    if colors() is True:
        try:
            try:
                browser.find_element_by_id("onetrust-button-group-parent").click()
            except Exception:
                traceback.print_exc()

            def get_colors_list():
                color_container = browser.find_element_by_class_name(
                    "select-color-container"
                )
                return color_container.find_elements_by_tag_name("a")

            colors = get_colors_list()
            ref = generate_product_ref()  # Выносим реф сюда, чтобы он был одинаковым
            # у продуктов разных цветов
            for color in colors:
                attempts = 0
                while attempts < 6:
                    try:
                        color.click()
                        break
                    except ElementClickInterceptedException:
                        close_popups()
                        color.click()
                    attempts = attempts + 1

                current_color = get_current_color()
                name = get_name()
                art = get_art()
                pictures = get_pictures()
                description = get_description()
                sizes = get_sizes()
                materials = get_materials()

                results_dict = dict(
                    url=url,
                    cat_id=cat,
                    ref=ref,
                    color=current_color,
                    name=name,
                    art=art,
                    pictures=pictures,
                    description=description,
                    sizes=sizes,
                    materials=materials,
                )

                results.append(results_dict)

        except WebDriverException as webdriver_exception:
            traceback.print_exc()
            print(get_current_time(), webdriver_exception, flush=True)
        except Exception:
            traceback.print_exc()

    else:
        try:
            try:
                browser.find_element_by_id("onetrust-button-group-parent").click()
            except Exception:
                traceback.print_exc()
            ref = generate_product_ref()
            name = get_name()
            art = get_art()
            pictures = get_pictures()
            description = get_description()
            sizes = get_sizes()
            materials = get_materials()

            results_dict = dict(
                url=url,
                cat_id=cat,
                ref=ref,
                color=None,
                name=name,
                art=art,
                pictures=pictures,
                description=description,
                sizes=sizes,
                materials=materials,
            )

            results.append(results_dict)

        except WebDriverException as webdriver_exception:
            print(get_current_time(), webdriver_exception, flush=True)
        except Exception:
            traceback.print_exc()

    browser.quit()

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

            shop_id = 4
            product_ref = result["ref"]
            parsed = ts
            updated = ts
            name = result["name"]
            available = 1
            brand = "Zara Home"
            art = result["art"]
            current_price = result["sizes"][0]["size_price"]
            currency = "EUR"
            description = result["description"]
            material = result["materials"]
            dimensions = str(result["sizes"])
            images = ", ".join(result["pictures"])
            img_main = result["pictures"][0]
            img_additional = ", ".join(result["pictures"])
            cat_id = result["cat_id"]
            color = result["color"]

            with connection.cursor() as cursor:
                insert_query = "INSERT INTO parsed_products (" \
                               "shop_id, url, product_ref, parsed, updated, name," \
                               " available, brand, art, current_price, currency," \
                               " description, material, dimensions," \
                               " images, img_main, img_additional, category, color)" \
                               " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                               " %s, %s, %s, %s, %s, %s, %s);"
                insert_values = (
                    shop_id, url, product_ref, parsed, updated, name, available,
                    brand, art, current_price, currency, description, material,
                    dimensions, images, img_main, img_additional, cat_id,
                    color
                )
                cursor.execute(insert_query, insert_values)

                connection.commit()
        except IndexError:
            pass

    connection.close()

    print(f"{get_current_time()} Product data has been collected!", flush=True)
    print("--- --- ---", flush=True)
    return results


if __name__ == "__main__":
    fetch_all_ref_codes()
    categories = get_categories_from_db()
    for category in categories:
        products = get_products(category)
        for product in products:
            try:
                product_data = get_product_data(product)
            except Exception:
                traceback.print_exc()
