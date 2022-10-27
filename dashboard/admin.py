from django.contrib import admin

# Register your models here.
from dashboard.models import Reportings,Process

admin.site.register(Process)
admin.site.register(Reportings)