import datetime

import pymysql

import config as cfg
from utils import ReadResults


class WriteResultsToDB:
    def __init__(self):
        connection = pymysql.connect(
            host=cfg.db_data["host"],
            user=cfg.db_data["user"],
            password=cfg.db_data["password"],
            db=cfg.db_data["db"],
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

        results = ReadResults().data

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
                category = result["cat_id"]
                color = result["color"]

                with connection.cursor() as cursor:
                    insert_query = "INSERT INTO parsed_products (" \
                                   "shop_id, product_ref, parsed, updated, name," \
                                   " available, brand, art, current_price, currency," \
                                   " description, material, dimensions," \
                                   " images, img_main, img_additional, category, color)" \
                                   " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                                   " %s, %s, %s, %s, %s, %s, %s);"
                    insert_values = (
                        shop_id, product_ref, parsed, updated, name, available,
                        brand, art, current_price, currency, description, material,
                        dimensions, images, img_main, img_additional, category, color
                    )
                    cursor.execute(insert_query, insert_values)

                    connection.commit()
            except IndexError:
                pass

        connection.close()
