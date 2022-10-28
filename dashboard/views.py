from os import abort
from traceback import print_tb
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

def home(request):
    return render(request, 'home.html')

@csrf_exempt
def process_status_table(request):
    if request.method=='GET':
        projects = Process.objects.all()
        return render(request, 'Displayprocess.html',{'projects':projects})
    
def update_status(request):
    if request.method=='POST':
        json_data=JSONParser().parse(request)
        process = Process.objects.filter(process_name= json_data["process_name"],computer_name= json_data["computer_name"]).first()
        if process :
            process["description"] = json_data["description"]
            process["status"] = json_data["status"]
            process["isrunning"] = json_data["isrunning"]
            process["customer_name"] = json_data["customer_name"]
            return JsonResponse("Changed Successfully",safe=False)
        process_serializer=ProcessSerializer(data=json_data)
        if process_serializer.is_valid():
            process_serializer.save()
            return JsonResponse("Added Successfully",safe=False)
        return JsonResponse("Failed to Add",safe=False)

@csrf_exempt
def process_log_table(request,customer):
    if request.method=='GET':
        
        logtable = Reportings.objects.all()
        # log_serializer=LogSerializer(logtable,many=True)
        # return JsonResponse(log_serializer.data,safe=False)
        log_data = []

        for log in logtable:
            dict_data = {'process_name':log.process.process_name,
                'computer_name':log.process.computer_name,
                'customer_name': log.process.customer_name,
                'timestamp':log.timestamp,
                'comment': log.comment,
                'reason': log.reason}
            log_data.append(dict_data)

        # เพิ่ม computer name กับ process name ในการ display
        # computer name = process.computer_name
        return render(request, 'DisplayLog.html',{'logtable':log_data})
    
def add_log(request):
    if request.method=='POST':
        # อ่าน body computer name กับ process name เพื่อไปหา Process object แล้ว save ลง process
        # process = Process.object.filter(computhe_name = "" && )
        log_data=JSONParser().parse(request)
        process = Process.objects.get(process_name=log_data["process_name"] , computer_name = log_data["computer_name"])
        log_serializer=LogSerializer(data={'process': process.pk,'timestamp':log_data["timestamp"],'comment':log_data["comment"],'reason':log_data["reason"]})

        if log_serializer.is_valid():
            log_serializer.save()
            return JsonResponse("Added Successfully",safe=False)
        return JsonResponse(log_serializer.errors,safe=False)
    

@csrf_exempt
def linewebhook(request):
    if request.method == 'POST':
        print(request.body.decode())
        NotifyMessage()
        return JsonResponse(200,safe=False)
    if request.method == 'GET':
        return JsonResponse("Get method",safe=False)


@csrf_exempt
def NotifyMessage(message):
    LINE_API = 'https://api.line.me/v2/bot/message/push'

    Authorization = 'Bearer {}'.format(Line_accesstoken) ##ที่ยาวๆ
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization':Authorization
    }

    data = {
        "to": Group_id,
        "messages":[{
            "type":"text",
            "text":message
        }]
    }

    data = json.dumps(data) ## dump dict >> Json Object
    r = requests.post(LINE_API, headers=headers, data=data)
    return 200


# @csrf_exempt
# def departmentApi(request,id=0):
#     if request.method=='GET':
#         departments = Departments.objects.all()
#         departments_serializer=DepartmentSerializer(departments,many=True)
#         return JsonResponse(departments_serializer.data,safe=False)
#     elif request.method=='POST':
#         department_data=JSONParser().parse(request)
#         departments_serializer=DepartmentSerializer(data=department_data)
#         if departments_serializer.is_valid():
#             departments_serializer.save()
#             return JsonResponse("Added Successfully",safe=False)
#         return JsonResponse("Failed to Add",safe=False)
#     elif request.method=='PUT':
#         department_data=JSONParser().parse(request)
#         department=Departments.objects.get(DepartmentId=department_data['DepartmentId'])
#         departments_serializer=DepartmentSerializer(department,data=department_data)
#         if departments_serializer.is_valid():
#             departments_serializer.save()
#             return JsonResponse("Updated Successfully",safe=False)
#         return JsonResponse("Failed to Update")
#     elif request.method=='DELETE':
#         department=Departments.objects.get(DepartmentId=id)
#         department.delete()
#         return JsonResponse("Deleted Successfully",safe=False)

# @csrf_exempt
# def employeeApi(request,id=0):
#     if request.method=='GET':
#         employees = Employees.objects.all()
#         employees_serializer=EmployeeSerializer(employees,many=True)
#         return JsonResponse(employees_serializer.data,safe=False)
#     elif request.method=='POST':
#         employee_data=JSONParser().parse(request)
#         employees_serializer=EmployeeSerializer(data=employee_data)
#         if employees_serializer.is_valid():
#             employees_serializer.save()
#             return JsonResponse("Added Successfully",safe=False)
#         return JsonResponse("Failed to Add",safe=False)
#     elif request.method=='PUT':
#         employee_data=JSONParser().parse(request)
#         employee=Employees.objects.get(EmployeeId=employee_data['EmployeeId'])
#         employees_serializer=EmployeeSerializer(employee,data=employee_data)
#         if employees_serializer.is_valid():
#             employees_serializer.save()
#             return JsonResponse("Updated Successfully",safe=False)
#         return JsonResponse("Failed to Update")
#     elif request.method=='DELETE':
#         employee=Employees.objects.get(EmployeeId=id)
#         employee.delete()
#         return JsonResponse("Deleted Successfully",safe=False)

@csrf_exempt
def SaveFile(request):
    file=request.FILES['file']
    file_name=default_storage.save(file.name,file)
    return JsonResponse(file_name,safe=False)
