#!/usr/bin/env python
import os
import sys
import subprocess
from django.core.management import execute_from_command_line
from django.conf import settings


def get_ip():
    process = os.popen("ipconfig")
    proc = process.read()
    process.close()
    ip = ["", "fetching ip failed"]
    p = proc.split("\n")
    for line in p:
        if "IPv4" in line:
            ip = line.split(": ")

    return ip[1]


if __name__ == "__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoAPI.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    settings.MY_BASE_URL = f'http://{get_ip()}:8000/'
    print(settings.MY_BASE_URL)
    args = sys.argv
    args += [
        'runserver', '0.0.0.0:8000', '--noreload'
    ]
    execute_from_command_line(args)
