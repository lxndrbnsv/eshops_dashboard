import json

from app import db
from app.models import PlasticServices, BeautyServices


class WriteServicesToDB:
    def __init__(self):
        with open("./data/beauty/services.json", "r") as json_file:
            services_dict = json.load(json_file)

        print(len(services_dict))

        for sd in services_dict:
            print(sd)
            plastic_services = BeautyServices()
            plastic_services.service = sd["service"]
            plastic_services.service_id = sd["id"]
            plastic_services.host_service_name = sd["host_service_name"]

            db.session.add(plastic_services)
            db.session.commit()
