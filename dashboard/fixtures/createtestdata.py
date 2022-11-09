import datetime
import json
import random
import pytz
from django.utils import timezone

JSON = [
    {
        "model": "dashboard.process",
        "pk": 1,
        "fields": {
            "process_name": f"GW 1",
            "computer_name": f"computer name GW",
            "description": f"description GW",
            "status": 1,
            "isrunning": False,
            "customer_name": "Griffwerk",
        },
    },
    {
        "model": "dashboard.process",
        "pk": 2,
        "fields": {
            "process_name": "HA 1",
            "computer_name": f"computer name HA",
            "description": f"description HA",
            "status": 1,
            "isrunning": False,
            "customer_name": "Hafele",
        },
    },
]


def create_sample_data(entries=10, days=2, process=1):
    global JSON
    utc_now = datetime.datetime.utcnow()
    now = datetime.datetime.now()

    reports = []
    for day in reversed(range(days)):
        for entry in reversed(range(1, entries + 1)):
            reports.append(
                {
                    "model": "dashboard.reportings",
                    "fields": {
                        "process": process,
                        "comment": "some comment",
                        "reason": "reason",
                        "robot_timestamp": f"{(now - datetime.timedelta(days=day, hours=entry)).isoformat()}+03:00",
                        "server_timestamp": f"{(utc_now - datetime.timedelta(days=day, hours=entry)).isoformat()}+00:00",
                    },
                }
            )

    JSON = JSON + reports


def save_json(jsonfilename="data.json"):
    with open(f"dashboard/fixtures/{jsonfilename}", "w") as outfile:
        outfile.write(json.dumps(JSON, indent=4))


if __name__ == "__main__":
    # for process in JSON:
    #     create_sample_data(
    #         entries=5 * (process["pk"] * 2), days=2, process=process["pk"]
    #     )

    create_sample_data(entries=5, days=2, process=1)
    create_sample_data(entries=10, days=2, process=2)
    save_json()
