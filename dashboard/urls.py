from django.urls import include, re_path, path
from dashboard import views
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.home, name="home"),
    path("process/", views.process_status_table, name="process"),
    path("log/", views.all_log, name="alllog"),
    path("log/<str:customer>/", views.process_log_table, name="process_log_table"),
    path("log/<str:customer>/<str:process_name>/", views.process_view_log, name="process_view_log"),
    path("log/<str:customer>/<str:process_name>/filter_date_range/", views.process_view_log, name="process_view_log"),
    path("linewebhook/", views.linewebhook, name="linewebhook"),
    path("checkrunning/", views.checkrunning, name="checkrunning"),
    path("api/updatestatus/", views.update_status, name="update_status"),
    path("api/addlog/", views.add_log, name="add_log"),
    path("run_checks/", views.run_checks, name="run_checks"),
    path("hourly_run_checks/", views.hourly_run_checks, name="hourly_run_checks"),
]
