from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date

# Create your models here.


# Patient Register
class PatientRegister(models.Model):
    patient_id = models.AutoField(primary_key=True)
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=15)
    username = models.CharField(max_length=50)
    phone_number = models.BigIntegerField()
    email = models.EmailField(max_length=50)
    password1 = models.CharField(max_length=10)
    password2 = models.CharField(max_length=10)

    hospital_number = models.CharField(max_length=20, default="", blank=True)
    dateofbirth = models.CharField(max_length=10, default="")
    address = models.TextField(default="", blank=True)
    postcode = models.CharField(max_length=10, default="")

    time_stamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    forget_password_token = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = "patient_reg"


# Doctor Register
class DoctorRegister(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    patient_fk = models.ForeignKey(PatientRegister, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone_number = models.BigIntegerField()
    hospital_address = models.TextField()
    password1 = models.CharField(max_length=10)
    password2 = models.CharField(max_length=10)

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
    year_pain_began = models.CharField(max_length=20, blank=True)
    onset_of_pain = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=20)
    comments = models.TextField(blank=True)

    class Meta:
        db_table = "pain_details"


# Pain Start Table
class PainStartTable(models.Model):
    # patient_fk = models.ForeignKey(PatientRegister,on_delete=models.CASCADE)
    accident_at_work = models.CharField(max_length=20, blank=True)
    accident_at_home = models.CharField(max_length=20, blank=True)
    following_illness = models.CharField(max_length=20, blank=True)
    following_surgery = models.CharField(max_length=20, blank=True)
    road_traffic_accident = models.CharField(max_length=20, blank=True)
    pain_just_began = models.CharField(max_length=20, blank=True)
    others = models.TextField(blank=True)

    class Meta:
        db_table = "pain_start"


# Pain Type Table
class PainTypeTable(models.Model):
    throbbing = models.BooleanField(default=False, blank=True)
    shooting = models.BooleanField(default=False, blank=True)
    stabbing = models.BooleanField(default=False, blank=True)
    sharp = models.BooleanField(default=False, blank=True)
    cramping = models.BooleanField(default=False, blank=True)
    gnawing = models.BooleanField(default=False, blank=True)
    hot_burning = models.BooleanField(default=False, blank=True)
    aching = models.BooleanField(default=False, blank=True)
    heavy = models.BooleanField(default=False, blank=True)
    tender = models.BooleanField(default=False, blank=True)
    splitting = models.BooleanField(default=False, blank=True)
    tiring_exhausting = models.BooleanField(default=False, blank=True)
    sickening = models.BooleanField(default=False, blank=True)
    fearful = models.BooleanField(default=False, blank=True)
    pushing_cruel = models.BooleanField(default=False, blank=True)

    class Meta:
        db_table = "pain_type"
