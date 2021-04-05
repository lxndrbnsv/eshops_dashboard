import json

from app import db
from app.models import PlasticServices, BeautyServices


class WriteServicesToDB:
    def __init__(self):
        with open("./data/surgery/services.json", "r") as json_file:
            services_dict = json.load(json_file)

        print(len(services_dict))

        for sd in services_dict:
            print(sd)
            plastic_services = PlasticServices()
            plastic_services.service = sd["service"]
            plastic_services.service_id = sd["id"]
            plastic_services.host_service_name = sd["host_service_name"]

            db.session.add(plastic_services)
            db.session.commit()


class ManagePlasticDescriptions:
    def __init__(self):
        plastic_services = PlasticServices.query.all()

        for p in plastic_services:
            if p.description is None:
                if "(" in p.service:
                    print(p.service)
                    description = p.service.rsplit("(", 1)[1].rsplit(")", 1)[0]
                    p.description = description
                    db.session.commit()


class ManageBeautyDescriptions:
    def __init__(self):
        beauty_services = BeautyServices.query.all()

        for b in beauty_services:
            if b.description is None:
                if "(" in b.service:
                    print(b.description)
                    print(b.service)
                    description = b.service.rsplit("(", 1)[1].rsplit(")", 1)[0]
                    b.description = description
                    db.session.commit()


class ExportPlasticToJSON:
    def __init__(self):
        plastic_services = PlasticServices.query.all()

        plastic_dicts = []

        for p in plastic_services:
            plastic_dicts.append(
                dict(
                    service=p.service,
                    id=p.id,
                    description=p.description,
                    old_name=p.old_name
                )
            )

        new_data = json.dumps(plastic_dicts, indent=2, ensure_ascii=False)
        with open("./data/surgery/new_data/services.json", "w+") as json_file:
            json_file.write(new_data)


class ExportBeautyToJSON:
    def __init__(self):
        beauty_services = PlasticServices.query.all()

        beauty_dicts = []

        for b in beauty_services:
            beauty_dicts.append(
                dict(
                    service=b.service,
                    id=b.id,
                    description=b.description,
                    old_name=p.old_name
                )
            )

        new_data = json.dumps(beauty_dicts, indent=2, ensure_ascii=False)
        with open("./data/beauty/new_data/services.json", "w+") as json_file:
            json_file.write(new_data)
