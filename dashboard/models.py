from django.db import models


class Process(models.Model):
    id = models.AutoField(primary_key=True)
    process_name = models.CharField(max_length=500)
    computer_name = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
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
    robot_timestamp = models.CharField()
    server_timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.process.process_name}"


# class Process_check_setting(models.Model):
