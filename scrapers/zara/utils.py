import json

import pymysql

import scrapers.zara.config as cfg

class ReadCategories:
    def __init__(self):
        with open("./scrapers/zara/categories.json", "r") as json_file:
            categories = json.load(json_file)

        cat_list = []

        for c in categories:
            cat_list.append(c["cat"])

        self.categories = cat_list
        self.cat_dicts = categories


class WriteProductsJson:
    def __init__(self, dicts):
        try:
            with open("./scrapers/zara/products.json", "r") as json_file:
                existing_products = json.load(json_file)

            products = []

            for e in existing_products:
                products.append(e)
        except FileNotFoundError:
            products = []

        for product_dict in dicts:
            products.append(product_dict)
        products_to_write = json.dumps(products, indent=2, ensure_ascii=False)

        with open("./scrapers/zara/products.json", "w+") as json_file:
            json_file.write(products_to_write)


class ReadProducts:
    def __init__(self):
        with open("./scrapers/zara/products.json", "r") as json_file:
            json_data = json.load(json_file)
        self.dicts = json_data


class IfDuplicates:
    def __init__(self):
        with open("./scrapers/zara/products.json", "r") as json_file:
            products_dict = json.load(json_file)

        dicts_len = len(products_dict)

        links = []
        for product_dict in products_dict:
            if product_dict["product_link"] not in links:
                links.append(product_dict["product_link"])

        unique_len = len(links)

        if dicts_len - unique_len == 0:
            print("No duplicates found!", flush=True)
        else:
            print(dicts_len - unique_len, " duplicates found!")


class RemoveDuplicates:
    def __init__(self):
        with open("./scrapers/zara/products.json", "r") as json_file:
            products_dict = json.load(json_file)

        links = []
        new_data = []

        for product_dict in products_dict:
            if product_dict["product_link"] not in links:
                links.append(product_dict["product_link"])
                new_data.append(product_dict)

        data_to_write = json.dumps(new_data, indent=2, ensure_ascii=False)
        with open("scrapers/zara/products.json", "w") as json_file:
            json_file.write(data_to_write)


class WriteResults:
    def __init__(self, dicts):
        try:
            with open("./results.json", "r") as json_file:
                existing_products = json.load(json_file)

            products = []

            for e in existing_products:
                products.append(e)
        except FileNotFoundError:
            products = []

        for product_dict in dicts:
            products.append(product_dict)
        products_to_write = json.dumps(products, indent=2, ensure_ascii=False)

        with open("./results.json", "w+") as json_file:
            json_file.write(products_to_write)


class ReadResults:
    def __init__(self):
        with open("./results.json", "r") as json_file:
            self.data = json.load(json_file)


class RemoveDuplicateResults:
    def __init__(self):
        with open("./results.json", "r") as json_file:
            results_data = json.load(json_file)

        checked = []
        new_data = []

        for r in results_data:
            if r["pictures"] not in checked:
                new_data.append(r)
            checked.append(r["pictures"])

        print(len(results_data))
        print(len(new_data))

        json_data = json.dumps(new_data, indent=2, ensure_ascii=False)

        with open("./results.json", "w") as json_file:
            json_file.write(json_data)


class DownloadPictures:
    # TODO: загрузка картинок будет производиться уже после размещения парсера
    # на сервере.
    pass


class FixCategories:
    def __init__(self):
        print("Hello")

        connection = pymysql.connect(
            host=cfg.db_data["host"],
            user=cfg.db_data["user"],
            password=cfg.db_data["password"],
            db=cfg.db_data["db"],
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

        with connection.cursor() as cursor:
            select_query = "SELECT * FROM parsed_products;"
            cursor.execute(select_query)
            values = cursor.fetchall()

            #for v in values:
            ##    update_query = "UPDATE parsed_products SET product_ref=%s WHERE art=%s;"
            #    cursor.execute(update_query, (v["product_ref"], v["art"]))
            #    print("changed")
            #    connection.commit()

            values_1 = cursor.fetchall()
            values_2 = values_1
            for v1 in values_1:
                for v2 in values_2:
                    if v1["art"] == v2["art"] and v1["product_ref"] != v2["product_ref"]:
                        print("Match!")


            #connection.commit()
            connection.close()
