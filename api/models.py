from operator import mod
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# Patient Register
class PatientRegister(models.Model):
    patient_id = models.AutoField(primary_key=True)
    auth_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=15)
    username = models.CharField(max_length=50)
    phone_number = models.BigIntegerField()
    email = models.EmailField(max_length=50)
    password1 = models.CharField(max_length=10)
    password2 = models.CharField(max_length=10)
    hospital_number = models.CharField(max_length=20, default="")
    dateofbirth = models.CharField(max_length=10, default="")
    address = models.TextField(default="")
    postcode = models.CharField(max_length=10, default="")

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
    year_pain_began = models.IntegerField()
    onset_of_pain = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    comments = models.TextField()
    
    class Meta:
        db_table = "pain_details"


# Pain Start Table
class PainStartTable(models.Model):
    accident_at_work = models.BooleanField(default=False)
    accident_at_home = models.BooleanField(default=False)
    following_illness = models.BooleanField(default=False)
    following_surgery = models.BooleanField(default=False)
    road_traffic_accident = models.BooleanField(default=False)
    pain_just_began = models.BooleanField(default=False)
    others = models.TextField()

    class Meta:
        db_table = "pain_start"


# Pain Type Table
class PainTypeTable(models.Model):
    throbbing = models.BooleanField(default=False)
    shooting = models.BooleanField(default=False)
    stabbing = models.BooleanField(default=False)
    sharp = models.BooleanField(default=False)
    cramping = models.BooleanField(default=False)
    gnawing = models.BooleanField(default=False)
    hot_burning = models.BooleanField(default=False)
    aching = models.BooleanField(default=False)
    heavy = models.BooleanField(default=False)
    tender = models.BooleanField(default=False)
    splitting = models.BooleanField(default=False)
    tiring_exhausting = models.BooleanField(default=False)
    sickening = models.BooleanField(default=False)
    fearful = models.BooleanField(default=False)
    pushing_cruel = models.BooleanField(default=False)

    class Meta:
        db_table = "pain_type"
