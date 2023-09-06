{#
The mongodb seeder module. If 'mongodb' is selected,
this will be moved to  `src/flask/flaskapp/seeder.py`.
#}
import json

import models


def seed_data(filename:str, drop:bool=False) -> None:
    """Uses the json file to populate the database"""

    pk_maps = {}

    with open(filename) as f:
        data = json.load(f)

        if drop:
            models.Destination.drop_collection()
            models.Cruise.drop_collection()
            models.InfoRequest.drop_collection()

        for entry in data:
            if entry["model"] == "relecloud.destination":

                if models.Destination.objects.filter(name=entry["fields"]["name"]).count() == 0:
                    destination = models.Destination(
                        name=entry["fields"]["name"],
                        description=entry["fields"].get("description", None),
                        subtitle=entry["fields"].get("subtitle", None),
                    )
                    destination.save()
                    pk_maps[entry['pk']] = destination.id

            if entry["model"] == "relecloud.cruise":

                if models.Cruise.objects.filter(name=entry["fields"]["name"]).count() == 0:
                    cruise = models.Cruise(
                    name=entry["fields"]["name"],
                    description=entry["fields"].get("description", None),
                    subtitle=entry["fields"].get("subtitle", None),
                    )

                for destination_id in entry["fields"]["destinations"]:
                    destination = models.Destination.objects.get(id=pk_maps[destination_id])
                    cruise.destinations.append(destination)

                cruise.save()
