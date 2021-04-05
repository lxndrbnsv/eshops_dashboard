import json

from app import db
from app.models import BeautyServices


class ReadHostServicesBeauty:
    def __init__(self):
        with open("./data/beauty/services_id.json") as json_file:
            self.services = json.load(json_file)


class ReadServicesDictBeauty:
    def __init__(self):
        with open("./data/beauty/services.json") as json_file:
            self.services = json.load(json_file)


class AssignCategoryBeauty:
    def __init__(self, old_value, new_value):
        with open("./data/beauty/services_id.json") as json_file:
            services_id = json.load(json_file)

        services = BeautyServices().query.all()

        for s_id in services_id:
            if s_id["service"].strip() == new_value.split(" (", 1)[0].strip():
                for s in services:
                    if s.service == old_value:
                        s.service = new_value
                        s.service_id = s_id["id"]
                        s.old_name = old_value
                        s.host_service_name = s_id["service"]
                        try:
                            s.description = old_value.split("(", 1)[1].rsplit(")", 1)[0]
                        except IndexError:
                            s.description = None

                        db.session.commit()
