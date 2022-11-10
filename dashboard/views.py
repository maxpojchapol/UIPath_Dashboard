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
from dashboard.checks.run_checks import check_bots

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
def process_log_table(request, customer):
    if request.method == "GET":

        logtable = Reportings.objects.all()
        # log_serializer=LogSerializer(logtable,many=True)
        # return JsonResponse(log_serializer.data,safe=False)
        log_data = []

        for log in logtable:
            if log.process.customer_name == customer:
                dict_data = {
                    "process_name": log.process.process_name,
                    "computer_name": log.process.computer_name,
                    "customer_name": log.process.customer_name,
                    "timestamp": log.server_timestamp,
                    "comment": log.comment,
                    "reason": log.reason,
                }
                log_data.append(dict_data)

        # เพิ่ม computer name กับ process name ในการ display
        # computer name = process.computer_name
        return render(request, "DisplayLog.html", {"logtable": log_data})


@csrf_exempt
def add_log(request, jsonparser):
    if request.method == "POST":
        # อ่าน body computer name กับ process name เพื่อไปหา Process object แล้ว save ลง process
        # process = Process.object.filter(computhe_name = "" && )
        # log_data=JSONParser().parse(request)
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
            }
        )

        if log_serializer.is_valid():
            log_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse(log_serializer.errors, safe=False)


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
    reports = Reportings.objects.all()
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
