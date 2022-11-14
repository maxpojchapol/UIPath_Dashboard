from rest_framework import serializers
from dashboard.models import *

# class DepartmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Departments
#         fields=('DepartmentId','DepartmentName')

# class EmployeeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Employees
#         fields=('EmployeeId','EmployeeName','Department','DateOfJoining','PhotoFileName')


class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = (
            "process_name",
            "computer_name",
            "description",
            "status",
            "isrunning",
            "customer_name",
        )


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reportings
        fields = (
            "process", 
            "robot_timestamp", 
            "comment", 
            "reason")
