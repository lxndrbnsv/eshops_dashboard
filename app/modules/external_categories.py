import json

import pymysql.cursors


class GetExternalCategories:
    def __init__(self):
        connection = pymysql.connect(
            host="downlo04.mysql.tools",
            user="downlo04_parseditems",
            password="cu2%&52NzS",
            db="downlo04_parseditems",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

        try:
            with connection.cursor() as cursor:
                sql = (
                    "SELECT * FROM shop_category"
                )
                cursor.execute(sql)
                results = cursor.fetchall()

        finally:
            connection.close()

        categories = []

        for result in results:
            result_data = dict(
                name=result["name"],
                name_ru=result["name_ru"],
                cat_id=result["id"],
                parent_id=result["parent_id"]
            )
            categories.append(result_data)

        self.categories = categories


class WriteExternalCategories:
    def __init__(self, categories):
        json_data = json.dumps(categories, ensure_ascii=False)
        with open("./data/external_categories.json", "w+") as json_file:
            json_file.write(json_data)


class LoadExternalCategories:
    def __init__(self):
        with open("./data/external_categories.json", "r") as json_file:
            json_data = json.load(json_file)

        self.categories = json_data
