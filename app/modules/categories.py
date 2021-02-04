from app.models import ScraperCategory
from app.modules.external_categories import LoadExternalCategories


class LoadCategories:
    def __init__(self, shop_name):
        cat_dict = []
        for s in ScraperCategory.query.filter_by(shop=shop_name).all():
            cat_dict.append(
                dict(cat_link=s.cat_link, cat_id=s.cat_id, cat_name=s.cat_name)
            )
        self.categories = cat_dict


class CompareCategories:
    def __init__(self, keyword):
        external_categories = LoadExternalCategories().categories

        for e in external_categories:
            if keyword == e["name"]:
                self.cat_id = e["cat_id"]
                break
