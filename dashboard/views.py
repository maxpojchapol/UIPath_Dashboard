from formatter import test
from http.client import HTTPResponse
from os import abort
from traceback import print_tb
from xmlrpc.client import DateTime
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from dashboard.models import *
from dashboard.serializers import *
from Config.LineConfig import *

from django.core.files.storage import default_storage
import requests
import json
import datetime
from dashboard.checks.run_checks import *

from django.db.models import Q

# from datetime import timedelta
from django.utils import timezone


def home(request):
    return render(request, "home.html")


@csrf_exempt
def process_status_table(request):
    if request.method == "GET":
        projects = Process.objects.all()
        return render(request, "Displayprocess.html", {"projects": projects})


@csrf_exempt
def update_status(request):
    if request.method == "POST":
        json_data = JSONParser().parse(request)
        process = Process.objects.filter(
            process_name=json_data["process_name"],
            computer_name=json_data["computer_name"],
        ).first()
        if process:
            process.description = json_data["description"]
            process.status = json_data["status"]
            process.isrunning = json_data["isrunning"]
            process.customer_name = json_data["customer_name"]
            process.save()
            add_log(request, json_data)
            return JsonResponse("Changed Successfully", safe=False)
        # json_data["description"] = str(datetime.datetime.now())
        process_serializer = ProcessSerializer(
            data={
                "process_name": json_data["process_name"],
                "computer_name": json_data["computer_name"],
                "description": json_data["description"],
                "status": json_data["status"],
                "isrunning": json_data["isrunning"],
                "customer_name": json_data["customer_name"],
            }
        )
        if process_serializer.is_valid():
            process_serializer.save()
            add_log(request, json_data)
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)


@csrf_exempt
def process_log_table(request,customer):
    if request.method=='GET':
        
        logtable = Reportings.objects.filter(process__customer_name = customer)
        
        return render(request, 'DisplayLog.html',{'logtable':logtable})

@csrf_exempt
def process_view_log(request,customer,process_name):

    logtable = Reportings.objects.filter(process__customer_name=customer,process__process_name=process_name)
    process_name = process_name
    if request.method=='GET':
        total_transactions = 0
        mysum = datetime.timedelta()
        for element in logtable:
            (h, m, s) = str(element.robot_runtime).split(':')
            d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=float(s))
            mysum += d
            if isinstance(str(element.transaction_amount), int) or str(element.transaction_amount).isdigit():
                total_transactions += int(element.transaction_amount)
        return render(request, 'DisplayLog_filter.html',{'runtime_sum':mysum ,'logtable':logtable , 'process_name':process_name, 'total_transactions': total_transactions })
    else:
        date_from = datetime.datetime.strptime(str(request.POST["date_from"]),"%Y-%m-%d")
        date_to = datetime.datetime.strptime(str(request.POST["date_to"]),"%Y-%m-%d") 
        logtable = logtable.filter(
                Q(robot_timestamp__gte=date_from) & Q(robot_timestamp__lte=date_to+ datetime.timedelta(days=1))
            )
        total_transactions = 0
        mysum = datetime.timedelta()
        for element in logtable:
            (h, m, s) = str(element.robot_runtime).split(':')
            d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=float(s))
            mysum += d
            if isinstance(str(element.transaction_amount), int) or str(element.transaction_amount).isdigit():
                total_transactions += int(element.transaction_amount)
        
        

    return render(request, 'DisplayLog_filter.html',{'runtime_sum':mysum ,'logtable':logtable, 'process_name':process_name, 'total_transactions': total_transactions, 'date_from':datetime.datetime.strftime(date_from,"%m/%d/%Y"),'date_to': datetime.datetime.strftime(date_to,"%m/%d/%Y")})

@csrf_exempt
def all_log(request):
    if request.method=='GET':
        
        logtable = Reportings.objects.all()
        
        return render(request, 'DisplayLog.html',{'logtable':logtable})

@csrf_exempt    
def add_log(request,jsonparser=False):
    if request.method=='POST':
        # อ่าน body computer name กับ process name เพื่อไปหา Process object แล้ว save ลง process
        # process = Process.object.filter(computhe_name = "" && )
        # log_data=JSONParser().parse(request)
        if not jsonparser :
            log_data = JSONParser().parse(request)
            
        else:
            log_data = jsonparser

        process = Process.objects.get(
            process_name=log_data["process_name"],
            computer_name=log_data["computer_name"],
        )
        log_serializer = LogSerializer(
            data={
                "process": process.pk,
                "timestamp": datetime.datetime.now(),
                "comment": log_data["comment"],
                "reason": log_data["reason"],
                "robot_timestamp": log_data["robot_timestamp"],
                "transaction_amount" : log_data["transaction_amount"],
                "robot_runtime" : log_data["robot_runtime"]
            }
        )

        if log_serializer.is_valid():
            log_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse(log_serializer.errors, safe=False)
    elif request.method=='GET':
        logtable = Reportings.objects.all()
        return JsonResponse(logtable, safe=False)


@csrf_exempt
def linewebhook(request):
    if request.method == "POST":
        print(request.body.decode())
        # message = "test"
        # NotifyMessage(message)
        return JsonResponse(200, safe=False)
    if request.method == "GET":
        return JsonResponse("Get method", safe=False)


@csrf_exempt
def NotifyMessage(message):
    LINE_API = "https://api.line.me/v2/bot/message/push"

    Authorization = "Bearer {}".format(Line_accesstoken)
    print(Authorization)
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": Authorization,
    }

    data = {"to": Group_id, "messages": [{"type": "text", "text": message}]}

    data = json.dumps(data)  ## dump dict >> Json Object
    r = requests.post(LINE_API, headers=headers, data=data)
    return 200


@csrf_exempt
def checkrunning(request):
    json_data = JSONParser().parse(request)
    report_last = Reportings.objects.filter(
        process__process_name=json_data["process_name"],
        process__computer_name=json_data["computer_test_line"],
    ).last()
    if report_last.process.isrunning:
        message = "process still running since " + (
            report_last.server_timestamp
        ).strftime("%d-%m-%Y %H:%M:%S")
        NotifyMessage(message)
    elif timezone.make_naive(report_last.server_timestamp) < (
        datetime.datetime.now() - datetime.timedelta(hours=1)
    ):
        print("process is not running")
        message = "process is not running the lastest run was on " + (
            report_last.server_timestamp
        ).strftime("%d-%m-%Y %H:%M:%S")
        NotifyMessage(message)

    return JsonResponse("Report successfully", safe=False)
    # else:
    #     message = "process is successful running"
    #     # NotifyMessage(message)


@csrf_exempt
def SaveFile(request):
    file = request.FILES["file"]
    file_name = default_storage.save(file.name, file)
    return JsonResponse(file_name, safe=False)


def run_checks(request):
    reports = Reportings.objects.filter(reason = "End Process")
    process = Process.objects.all()
    res = check_bots(reports, process)
    # gt = Reportings.objects.filter(
    #     server_timestamp__gte=datetime.datetime.now(timezone.utc)
    #     - datetime.timedelta(days=2),
    #     process__id=1,
    # )
    # lt = Reportings.objects.filter(
    #     server_timestamp__lte=datetime.datetime.now(timezone.utc)
    #     - datetime.timedelta(days=2),
    #     process__id=1,
    # )

    return JsonResponse(res, safe=False)

def hourly_run_checks(request):
    reports = Reportings.objects.filter(reason = "Start run")
    process = Process.objects.all()
    res = hourly_check_bots(reports, process)

    return JsonResponse(res, safe=False)