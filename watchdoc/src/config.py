import os

from pathlib import Path

# ------------------------------------------------------------------------------
# Navigation

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
GENERATED_DIR = BASE_DIR / "generated"
TEMP_DIR = BASE_DIR / "temp"

# ------------------------------------------------------------------------------
# Internal

WATCHDOC_PORT = int(os.environ["WATCHDOC_PORT"])
WATCHDOC_AUTH_PORT = int(os.environ["WATCHDOC_AUTH_PORT"])

DEBUG = os.environ["DEBUG"].lower() == "true"

# ------------------------------------------------------------------------------
# Email settings

EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_PORT = os.environ["EMAIL_PORT"]
EMAIL_USE_TLS = os.environ["EMAIL_USE_TLS"].lower() == "true"
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
EMAIL_FROM_NAME = "Даль ВУЦ ВШЭ"

# ------------------------------------------------------------------------------
# YaDisk

YADISK_TOKEN = os.environ["YADISK_TOKEN"]
