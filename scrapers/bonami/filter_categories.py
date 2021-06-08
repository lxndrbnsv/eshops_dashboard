import json


if __name__ == "__main__":

    categories = []

    with open("categories.json", "r") as json_file:
        cat_data = json.load(json_file)

    for c in cat_data:
        if (
            "skladem" not in c["cat"]
            and "slevy" not in c["cat"]
            and "nordic" not in c["cat"]
            and "produkty" not in c["cat"]
            and "damske" not in c["cat"]
            and "panske" not in c["cat"]
        ):
            categories.append(c)

    json_data = json.dumps(categories)
    with open("categories.json", "w") as json_file:
        json_file.write(json_data)
