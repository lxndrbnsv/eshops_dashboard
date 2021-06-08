import sys
import traceback

from scrapers.zara.utils import ReadCategories, ReadProducts, WriteResults
from scrapers.zara.scraper import GetProductLinks, GetProductData
from scrapers.zara.db import WriteResultsToDB


sys.stdout = open("logs.log", "w")
sys.stderr = open("logs.log", "w")


class Zara:
    def __init__(self):
        categories = ReadCategories().cat_dicts
        for category in categories:
            GetProductLinks(category)
        products = ReadProducts().dicts
        for product in products:
            try:
                WriteResultsToDB(GetProductData(product).results)
            except Exception:
                traceback.print_exc()
                pass
