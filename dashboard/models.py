from django.db import models

class Process(models.Model):
    id = models.AutoField(primary_key=True)
    process_name = models.CharField(max_length=500)
    computer_name = models.CharField(max_length=500,null=True,blank=True)
    description = models.CharField(max_length=500,null=True,blank=True)
    status = models.IntegerField(null=True,blank=True)
    isrunning = models.BooleanField()
    customer_name = models.CharField(max_length=500)


class Reportings(models.Model):
    process = models.ForeignKey(Process, on_delete=models.CASCADE, null=False, blank=False)
    timestamp = models.DateTimeField()
    comment = models.CharField(max_length=500) # How many transaction, error screenshot
    reason = models.CharField(max_length=500)  # Robot run successfully, Robot start running, Robot face the problem
    

