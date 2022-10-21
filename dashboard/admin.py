from django.contrib import admin

# Register your models here.
from dashboard.models import Process,Reportings

admin.site.register(Process)
admin.site.register(Reportings)