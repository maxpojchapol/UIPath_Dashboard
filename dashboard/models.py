from django.db import models
import datetime


class Process(models.Model):
    id = models.AutoField(primary_key=True)
    process_name = models.CharField(max_length=500)
    computer_name = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    # status 1 = success
    # status 2 = common error
    # status 3 = uncommon error
    isrunning = models.BooleanField()
    customer_name = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.process_name}"


class Reportings(models.Model):
    process = models.ForeignKey(
        Process, on_delete=models.CASCADE, null=False, blank=False
    )
    comment = models.CharField(max_length=500)  # How many transaction, error screenshot
    reason = models.CharField(
        max_length=500
    )  # Robot run successfully, Robot start running, Robot face the problem
    robot_timestamp = models.DateTimeField()
    server_timestamp = models.DateTimeField(auto_now=True)  # auto_now=True for running the server
    robot_runtime = models.DurationField(null=True,blank=True)
    transaction_amount = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return f"{self.process.process_name}"


# class Process_check_setting(models.Model):
