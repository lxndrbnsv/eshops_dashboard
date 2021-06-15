import pymysql

import scrapers_config as cfg


print("Connecting...")
connection = pymysql.connect(
            host=cfg.db_data["host"],
            user=cfg.db_data["user"],
            password=cfg.db_data["password"],
            db=cfg.db_data["db"],
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

with connection.cursor() as cursor:
    select_query = "SELECT id, product_ref, url FROM parsed_products WHERE shop_id=5;"
    cursor.execute(select_query)

    ids_to_change = []
    ids_to_save = []
    all_zara_items = cursor.fetchall()
    print("Items has been fetched...")
    items_to_check = all_zara_items
    print("Comparing....")
    for a in all_zara_items:
        for b in items_to_check:
            if a["product_ref"] != b["product_ref"] and a["url"] == b["url"]:
                if b["id"] not in ids_to_change:
                    ids_to_change.append((b["id"], a["product_ref"]))

    print("Done!")
    print("Fixing duplicates...")
    for item_id in ids_to_change:
        update_query = "UPDATE parsed_products SET product_ref=%s WHERE id=%s;"
        update_values = (item_id[1], item_id[0])
        cursor.execute(update_query, update_values)
    connection.commit()

    connection.close()
    print("Done!")
