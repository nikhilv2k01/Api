from . import views
from django.urls import path
from django.urls import re_path as url

urlpatterns = [
    url(r'^patient/register$', views.patient_register),
    url(r'^patient/login$', views.patient_login),
    path('patient/display/update/<int:id>', views.patient_display_update),


    url(r'^tech/register$', views.tech_register),
    url(r'^tech/login$', views.tech_login),
    url(r'^tech/display$', views.tech_display),


    url(r'^doctor/register$', views.doctor_register),
    url(r'^doctor/login$', views.doctor_login),
    url(r'^doctor/display$', views.doctor_display),

    url(r'^pain-details$', views.pain_details),
    url(r'^pain-start$', views.pain_start),
    url(r'^pain-type$', views.pain_type),

    # url(r'^forget-password/$', views.forget_password),
    # path('change-password/<token>/', views.change_password),

     path(
        "reset-password/",
        views.PasswordReset.as_view(),
        name="reset-password",
    ),
    path(
        "change-password/<str:encoded_pk>/<str:token>/",
        views.ResetPasswordAPI.as_view(),
        name="reset-password",
    ),
]
