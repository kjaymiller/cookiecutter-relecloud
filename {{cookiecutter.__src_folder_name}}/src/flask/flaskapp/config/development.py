import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

{% if 'postgres' in cookiecutter.db_resource %}
dbuser = os.environ["POSTGRES_USERNAME"]
dbpass = os.environ["POSTGRES_PASSWORD"]
dbhost = os.environ["POSTGRES_HOST"]
dbname = os.environ["POSTGRES_DATABASE"]
DATABASE_URI = f"postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}"
{% endif %}

{% if 'mongo' in cookiecutter.db_resource %}
dbuser = os.environ["MONGO_USERNAME"]
dbpass = os.environ["MONGO_PASSWORD"]
dbhost = os.environ["MONGO_HOST"]
dbname = os.environ["MONGO_DATABASE"]
DATABASE_URI  = f"mongodb://{dbuser}:{dbpass}@{dbhost}/{dbname}"
{% endif %}
TIME_ZONE = "UTC"
