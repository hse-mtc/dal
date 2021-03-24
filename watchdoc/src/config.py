import os

from pathlib import Path

# ------------------------------------------------------------------------------
# Navigation

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
GENERATED_DIR = BASE_DIR / "generated"

# ------------------------------------------------------------------------------
# Google Auth

CREDENTIALS_PATH = BASE_DIR / "service-account.json"
SCOPES = [
    "https://www.googleapis.com/auth/drive",
]

# ------------------------------------------------------------------------------
# Internal

ADMIN_EMAIL = os.environ["ADMIN_EMAIL"]
WATCHDOC_PORT = int(os.environ["WATCHDOC_PORT"])
