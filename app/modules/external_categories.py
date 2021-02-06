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

            categories = []
            for result in results:
                with connection.cursor() as cursor:
                    try:
                        select_query = (
                            "SELECT name, name_ru FROM shop_category WHERE"
                            " id = %s"
                        )
                        cursor.execute(select_query, result["parent_id"])
                        parent_data = cursor.fetchone()
                        if parent_data is None:
                            parent_data = dict(name=None, name_ru=None)
                    except Exception:
                        parent_data = dict(name=None, name_ru=None)
                result_data = dict(
                    name=result["name"],
                    name_ru=result["name_ru"],
                    cat_id=result["id"],
                    parent_id=result["parent_id"],
                    parent_name=parent_data["name"],
                    parent_name_ru=parent_data["name_ru"]
                )
                categories.append(result_data)

        finally:
            connection.close()

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
