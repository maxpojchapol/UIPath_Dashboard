from dashboard.checks.check_config import CHECKS
import datetime
from django.utils.timezone import timezone


def check_bots(reports, process):
    results = ["results here append dicts with messages"]
    last_24 = reports.filter(
        server_timestamp__lte=datetime.datetime.now(timezone.utc)
        - datetime.timedelta(days=1)
    )

    for check in CHECKS:
        if check.get("daily_expected"):
            daily_check(check, last_24, process)

    return results


def daily_check(check, last_24, process):
    in_db = last_24.filter(process__process_name=check["process"]).count()
    if in_db < check["daily_expected"]:
        print(
            f"""notify_message daily check
              {check["process"]}: {in_db}/{check["daily_expected"]}"""
        )
