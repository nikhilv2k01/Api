from . import views
from django.urls import path
from django.urls import re_path as url

urlpatterns = [
    url(r'^patient/register$', views.patient_register),
    url(r'^patient/login$', views.patient_login),
    url(r'^patient/display/update$', views.patient_display_update),


    # url(r'^tech/register$', views.tech_register),
    # url(r'^tech/login$', views.tech_login),
    # url(r'^tech/display$', views.tech_display),


    # url(r'^doctor/register$', views.doctor_register),
    # url(r'^doctor/login$', views.doctor_login),
    # url(r'^doctor/display$', views.doctor_display),

    url(r'^painDetails$',views.pain_details),
    url(r'^painStart$',views.pain_start),
    url(r'^painType$',views.pain_type),
]
