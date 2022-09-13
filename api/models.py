from time import time
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date

# Create your models here.


# Patient Register
class PatientRegister(models.Model):
    patient_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=15)
    username = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    password1 = models.CharField(max_length=10)
    password2 = models.CharField(max_length=10)

    hospital_number = models.CharField(max_length=20, default="", blank=True)
    dateofbirth = models.CharField(max_length=10, default="")
    address = models.TextField(default="", blank=True)
    postcode = models.CharField(max_length=10, default="")

    is_verified = models.BooleanField(default=False)
    auth_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    time_stamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = "patient_reg"

 
# Doctor Register
class DoctorRegister(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    # patient_fk = models.ForeignKey(PatientRegister, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    username = models.CharField(max_length=50)
    specialization  = models.CharField(max_length=150)
    hospital_id  = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=20)
    password1 = models.CharField(max_length=20)
    password2 = models.CharField(max_length=20)

    class Meta:
        db_table = "doctor_reg"


# Tech Support Register
class TechRegister(models.Model):
    tech_id = models.AutoField(primary_key=True)
    patient_fk = models.ForeignKey(PatientRegister, on_delete=models.CASCADE)
    doctor_fk = models.ForeignKey(DoctorRegister, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone_number = models.BigIntegerField()
    address = models.TextField()
    password1 = models.CharField(max_length=10)
    password2 = models.CharField(max_length=10)

    class Meta:
        db_table = "tech_reg"


# Pain Details
class PainDetails(models.Model):
    patient_fk  = models.ForeignKey(PatientRegister,on_delete=models.CASCADE)
    year_pain_began = models.CharField(max_length=20, blank=True)
    onset_of_pain = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=20)
    comments = models.TextField(blank=True)

    class Meta:
        db_table = "pain_details"


# Pain Start Table
class PainStartTable(models.Model):
    patient_fk = models.ForeignKey(PatientRegister,on_delete=models.CASCADE)
    accident_at_work = models.CharField(max_length=3, blank=True)
    accident_at_home = models.CharField(max_length=3, blank=True)
    following_illness = models.CharField(max_length=3, blank=True)
    following_surgery = models.CharField(max_length=3, blank=True)
    road_traffic_accident = models.CharField(max_length=3, blank=True)
    pain_just_began = models.CharField(max_length=3, blank=True)
    others = models.TextField(blank=True)

    class Meta:
        db_table = "pain_start"


# Pain Type Table
class PainTypeTable(models.Model):
    patient_fk  = models.ForeignKey(PatientRegister,on_delete=models.CASCADE)
    throbbing = models.CharField(max_length=3, blank=True)
    shooting = models.CharField(max_length=3,  blank=True)
    stabbing = models.CharField(max_length=3,  blank=True)
    sharp = models.CharField(max_length=3,  blank=True)
    cramping = models.CharField(max_length=3,  blank=True)
    gnawing = models.CharField(max_length=3,  blank=True)
    hot_burning = models.CharField(max_length=3,  blank=True)
    aching = models.CharField(max_length=3,  blank=True)
    heavy = models.CharField(max_length=3,  blank=True)
    tender = models.CharField(max_length=3,  blank=True)
    splitting = models.CharField(max_length=3,  blank=True)
    tiring_exhausting = models.CharField(max_length=3, blank=True)
    sickening = models.CharField(max_length=3,  blank=True)
    fearful = models.CharField(max_length=3,  blank=True)
    pushing_cruel = models.CharField(max_length=3,  blank=True)

    class Meta:
        db_table = "pain_type"
