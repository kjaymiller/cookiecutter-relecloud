"""Adds the documents from a json_file to the database"""
import json

import models

pk_maps = {}

def seed_data(filename:str) -> None:
    """Uses the json file to populate the database"""
    with open(filename) as f:
        data = json.load(f)

        for entry in data:
            if entry["model"] == "relecloud.destination":
                destination = models.Destination(
                    name=entry["fields"]["name"],
                    description=entry["fields"].get("description", None),
                    subtitle=entry["fields"].get("subtitle", None),
                )
                destination.save()
                pk_maps[entry['pk']] = destination.id

            if entry["model"] == "relecloud.cruise":
                cruise = models.Cruise(
                    name=entry["fields"]["name"],
                    description=entry["fields"].get("description", None),
                    subtitle=entry["fields"].get("subtitle", None),
                )
                    
                for destination_id in entry["fields"]["destinations"]:
                    destination = models.Destination.objects.get(id=pk_maps[destination_id])
                    cruise.destinations.append(destination)

                cruise.save()