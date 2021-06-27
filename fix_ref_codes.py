import pymysql

import scrapers_config as cfg


connection = pymysql.connect(
            host=cfg.db_data["host"],
            user=cfg.db_data["user"],
            password=cfg.db_data["password"],
            db=cfg.db_data["db"],
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

with connection.cursor() as cursor:
    select_query = "SELECT product_ref FROM parsed_products;"
    cursor.execute(select_query)
    fetched_data = cursor.fetchall()
    print(len(fetched_data))
    all_ref_codes = []
    single_ref_codes = []
    for f in fetched_data:
        if f["product_ref"] not in all_ref_codes:
            all_ref_codes.append(f["product_ref"])
    print(len(all_ref_codes))
    for a in all_ref_codes:
        if all_ref_codes.count(a) == 1 and a is not None:
            single_ref_codes.append(a)
    print("Single: ", len(single_ref_codes))
    for s in single_ref_codes:
        print(s)
    for ref_code in single_ref_codes:
        print(ref_code)
        ids = []
        select_query = "SELECT id FROM parsed_products WHERE product_ref=%s;"
        select_value = ref_code
        cursor.execute(select_query, select_value)
        products = cursor.fetchall()
        for p in products:
            if p["id"] not in ids:
                ids.append(p["id"])
        for i in ids:
            update_query = "UPDATE parsed_products SET product_ref = Null WHERE " \
                           "id=%s;"
            cursor.execute(update_query, i)

    connection.commit()
    connection.close()
