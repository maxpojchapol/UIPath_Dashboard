import datetime
import json
def create_sample_data(timestart,timeend,timegap,jsonfilename):
    json_list = []
    json_list.append({
      "model": "dashboard.process",
      "pk": 1,
      "fields": {
        "process_name": "GW Process 1",
        "computer_name": "prod",
        "description": "test process GW 1",
        "status": 1,
        "isrunning": False,
        "customer_name": "Griffwerk"    
      }
    })
    dt_timestart = datetime.datetime.strptime(timestart,'%d/%m/%y %H:%M:%S')
    dt_timeend = datetime.datetime.strptime(timeend,'%d/%m/%y %H:%M:%S')
    int_timegap = int(timegap)
    while dt_timestart<=dt_timeend:
        json_list.append({
      "model": "dashboard.reportings",
      "fields": {
        "process": 1,
        "comment": "some comment",
        "reason": "reason",
        "robot_timestamp": str(dt_timestart)+"+03:00",
        "server_timestamp": str(dt_timestart)+"+00:00"
      }
        })
        dt_timestart = dt_timestart + datetime.timedelta(hours=int_timegap)
    print("")
    with open(jsonfilename, "w") as outfile:
        outfile.write(json.dumps(json_list))

create_sample_data("11/08/22 10:55:26","11/08/22 13:55:26",1,"sample.json")