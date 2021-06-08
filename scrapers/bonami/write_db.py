import datetime
import traceback

import pymysql.cursors


class WriteProducts:
    def __init__(self, results):
        ts = datetime.datetime.now()

        # Подключаемся к БД.
        connection = pymysql.connect(
            host="downlo04.mysql.tools",
            user="downlo04_parseditems",
            password="cu2%&52NzS",
            db="downlo04_parseditems",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

        try:
            for r in results:
                try:
                    with connection.cursor() as cursor:
                        sql = "INSERT INTO parsed_products " \
                              "(shop_id, product_ref, parsed , updated, url," \
                              " name, available, " \
                              "brand, art," \
                              " current_price, currency, " \
                              "description, material, dimensions, " \
                              "length, height, width, volume, images, " \
                              "img_main, img_additional,  " \
                              "category, attr_other, " \
                              "image_main_url, image_additional_url, pwr, weight, old_price, discount, color) " \
                              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                              "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                              "%s, %s, %s, %s, %s, %s, %s, %s)"

                        cursor.execute(
                            sql, (
                                3, r["product_ref"],
                                ts,
                                ts,
                                r["url"], r["name"], r["available"],
                                None, r["art"],
                                r["price"]["new_price"], r["currency"],
                                r["description"], r["parameters"]["material"],
                                r["dimensions"], r["length"],
                                r["height"], r["width"],
                                None,
                                None,
                                r["img_main"], None, r["cat_id"], str(r["parameters"]),
                                r["img_main_url"],
                                None, None, r["weight"], r["old_price"], None, None

                            ),
                        )
                        connection.commit()
                except Exception:
                    traceback.print_exc()
        finally:
            connection.close()
            print("Done!")
