# boot_django.py
#
# This file sets up and configures Django. It's used by scripts that need to
# execute as if running in a Django server.
import os
import django
from django.conf import settings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "receipts"))

def boot_django():
    settings.configure(
        INSTALLED_APPS=(
            "relecloud",
        ),
        TIME_ZONE="UTC",
        USE_TZ=True,
    )
    django.setup()