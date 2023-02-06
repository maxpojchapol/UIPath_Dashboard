from dashboard.checks.check_config import CHECKS
import datetime
from django.utils.timezone import timezone

# This is for daily checking bot
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


# This is for hourly checking bot
def hourly_check_bots(reports, process):
    results = []
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
                results = hourly_check(check,last_hours,expect_run,process,results)

            # hourly_check(check,last_hours,expect_run,process)

    return results


def hourly_check(check, last_hours, expect_run, process,results):
    in_db = last_hours.filter(process__process_name=check["process"]).count()
    last_run = last_hours.filter(process__process_name=check["process"]).last()
    timeconvert = (datetime.datetime.combine(datetime.date(1,1,1),expect_run) + datetime.timedelta(hours=7)).time()
    if in_db < 1:
        results.append((f"""Notify_message hourly check
Process {check["process"]}is not running, robot should run at {timeconvert}"""))
              
    else:
        results.append((f"""Notify_message hourly check
Process {check["process"]}is run normally at {timeconvert}"""))
        # print(
        #     f"""notify_message hourly check
        #       Process is running normally at : {last_run.server_timestamp}"""
        # )
    return results


def hourly_check_error_bots(Report,Process):
    results = []
    report_last_hours = Report.objects.filter(
        server_timestamp__gte=datetime.datetime.now(timezone.utc)
        - datetime.timedelta(hours=1)
    )
    report_last_hours_error = list(report_last_hours.filter(reason__contains="Error"))
    for item in report_last_hours_error:
        results.append((f"""Notify_message hourly check
Process {item.process.process_name}is running and face the error with the reason
{item.reason}, please check the robot"""))
    #Notify message to the list

    return results