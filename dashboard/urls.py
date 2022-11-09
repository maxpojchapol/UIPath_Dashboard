from django.urls import include, re_path, path
from dashboard import views
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[

    path('',views.home, name='home'),
    
    path('process/', views.process_status_table , name='process'),
    path('log/', views.all_log , name='log'),
    path('log/<str:customer>/<str:process_name>/', views.process_view_log , name='process_view_log'),
    path('log/<str:customer>/', views.process_log_table , name='customer_log'),
    path('linewebhook/',views.linewebhook, name = 'linewebhook'),
    path('checkrunning/',views.checkrunning, name = 'checkrunning'),

    path('api/updatestatus/',views.update_status, name='update_status'),
    path('api/addlog/', views.add_log , name='addlog'),
    
    ]
