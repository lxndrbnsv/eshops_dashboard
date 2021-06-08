import sys
import os
import random
import string

import requests
import pymysql


sys.stdout = open("pic_logs.log", "w")
sys.stderr = open("pic_logs.log", "w")


def download_image(url, shop):
    print("*** *** ***")
    print("Downloading image: ", url)
    print("*** *** ***")

    def generate_name(characters):
        def generate():
            letters = string.ascii_letters
            digits = string.digits
            ref_code = "".join(
                random.choice(letters + digits) for __ in range(characters)
            )

            return ref_code

        value = generate()

        return value

    if not os.path.exists(f"./files/pics/{str(shop)}/"):
        os.makedirs(f"./files/pics/{str(shop)}/")

    image_files = os.listdir(f"./files/pics/{str(shop)}/")
    image_names = []
    for i in image_files:
        image_names.append(i.split(".", 1)[0])

    char_num = 1
    image_name = generate_name(char_num)
    while image_names in image_names:
        char_num = char_num + 1
        image_name = generate_name(char_num)

    r = requests.get(url)
    filename = f"{image_name}.jpg"
    filepath = f"./files/pics/{str(shop)}/{filename}"
    open(filepath, 'wb').write(r.content)

    return filename


connection = pymysql.connect(
    host="downlo04.mysql.tools",
    user="downlo04_parseditems",
    password="cu2%&52NzS",
    db="downlo04_parseditems",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
)

with connection.cursor() as cursor:
    sql_query = "SELECT id, shop_id, img_main, img_additional FROM parsed_products;"
    cursor.execute(sql_query)
    all_data = cursor.fetchall()
    for data in all_data:
        product_id = data["id"]
        img_main = data["img_main"]
        shop = data["shop_id"]
        main_image_name = download_image(img_main, shop)
        main_image_url = f"http://18.197.154.185/api/images/{str(shop)}/{main_image_name}"
        print(main_image_url)
        if data["img_additional"] != "" and data["img_additional"] is not None:
            imgs_additional = data["img_additional"].split(", ", 1)
            img_additional_urls_list = []
            for img_additional in imgs_additional:
                additional_image_name = download_image(img_additional, shop)
                additional_image_url = f"http://18.197.154.185/api/images/{str(shop)}/{additional_image_name}"
                img_additional_urls_list.append(additional_image_url)
            additional_images = ", ".join(img_additional_urls_list)
            print(additional_images)
        else:
            additional_images = None
        update_query = "UPDATE parsed_products SET image_main_url = %s, image_additional_url = %s WHERE id = %s;"
        update_values = (main_image_url, additional_images, product_id)
        cursor.execute(update_query, update_values)
        connection.commit()
    connection.close()
