import itertools
import sys
from datetime import datetime
import time
from pathlib import Path
from django.core.management import call_command

def run(*args):
    """
    This script implements database backup with a certain delay.
    """
    f_prefix = str(Path(__file__).resolve().parent.parent \
        / "dms/fixtures/backup")

    if len(args) > 2:
        raise ValueError("Too many arguments for backup")

    delay = 24 * 60 * 60  # Default delay is one day
    if "delay" in args:
        delay = int(args[1])
    for counter in itertools.count(start=1):
        if counter % delay == 0:
            datetime_suffix = datetime.now().strftime("%d-%m-%Y-%H:%M:%S")
            filename = f_prefix + "-date-" + datetime_suffix + ".json"

            sysout = sys.stdout
            sys.stdout = open(filename, "w")
            call_command("dumpdata", "--format=json")
            sys.stdout = sysout
            print("Successful backup on", datetime_suffix)

        time.sleep(1)
