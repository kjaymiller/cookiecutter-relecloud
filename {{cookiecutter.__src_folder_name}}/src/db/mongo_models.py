{#
The mongodb model definitions. If a 'mongodb' option is selected,
this will be moved to `src/models.py`.
#}
from mongoengine import (
    Document,
    EmailField,
    ListField,
    ReferenceField,
    StringField,
)

class Destination(Document):
    name = StringField(unique=True, required=True)
    subtitle = StringField(required=False)
    description = StringField(required=False)

    def __str__(self):
        return self.name

class Cruise(Document):
    name = StringField(unique=True, required=True)
    subtitle = StringField(required=False)
    description = StringField(required=False)
    destinations = ListField(
        ReferenceField(Destination),
    )

    def __str__(self):
        return self.name


class InfoRequest(Document):
    name = StringField(required=True)
    email = EmailField(required=True)
    notes = StringField(required=False)
    cruise = ReferenceField(Cruise)
