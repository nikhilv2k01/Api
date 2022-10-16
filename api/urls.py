from . import views
from django.urls import path
from django.urls import re_path as url

urlpatterns = [
    url(r'^patient/register$', views.patient_register, name="patient-register"),
    url(r'^patient/login$', views.patient_login),
    path('patient/display/<int:id>', views.patient_display),
    path('patient/update/<int:id>', views.patient_update),


    url(r'^tech/register$', views.tech_register),
    url(r'^tech/login$', views.tech_login),
    url(r'^tech/display$', views.tech_display),


    url(r'^doctor/register$', views.doctor_register),
    url(r'^doctor/login$', views.doctor_login),
    url(r'^doctor/display$', views.doctor_display),


    path('pain-selection/<int:id>', views.pain_selection),
    path('pain-details/<int:id>', views.pain_details),
    path('pain-details-display/<int:id>', views.pain_details_display),

    path(
        "reset-password/",
        views.PasswordReset.as_view(),
        name="reset-password",
    ),
    path(
        "change-password/<str:encoded_pk>/<str:token>/",
        views.ChangePassword.as_view(),
        name="reset-password",
    ),
    path('verify/<auth_token>', views.verify, name="verify"),
]
