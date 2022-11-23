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

def hourly_check_bots(reports, process):
    results = ["results here append dicts with messages"]
    last_hours_cal = datetime.datetime.now(timezone.utc)- datetime.timedelta(hours=1)
    last_hours = reports.filter(
        server_timestamp__gte=datetime.datetime.now(timezone.utc)
        - datetime.timedelta(hours=1)
    )

    for check in CHECKS:
        for expect_run in check.get("start_time_expect"):
            expect_run = datetime.datetime.strptime(expect_run,"%H:%M").time()
            print ("expect_run"+str(expect_run))
            print("now"+str(datetime.datetime.now(timezone.utc).time()))
            print("check time :"+ str(last_hours_cal))
            if (last_hours_cal.time() < expect_run < datetime.datetime.now(timezone.utc).time()):
                print("check")
                hourly_check(check,last_hours,expect_run,process)

            # hourly_check(check,last_hours,expect_run,process)

    return results


def hourly_check(check, last_hours, expect_run, process):
    in_db = last_hours.filter(process__process_name=check["process"]).count()
    last_run = last_hours.filter(process__process_name=check["process"]).last()
    if in_db < 1:
        print(
            f"""notify_message hourly check
              Process is not running last hours"""
        )
    else:
        print(
            f"""notify_message hourly check
              Process is runnind normally at : {last_run.server_timestamp}"""
        )
