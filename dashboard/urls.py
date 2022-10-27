from django.urls import include, re_path, path
from dashboard import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    # re_path(r'^department$',views.departmentApi),
    # re_path(r'^department/([0-9]+)$',views.departmentApi),

    # re_path(r'^employee$',views.employeeApi),
    # re_path(r'^employee/([0-9]+)$',views.employeeApi),

    path('process1/<int:id>/',views.process_status_table, name='process_status_table'),
    re_path(r'^addlog$',views.process_log_table),

    # re_path(r'^employee/savefile',views.SaveFile)
    ]
