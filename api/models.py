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
    auth_token = models.CharField(max_length=255)
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
    specialization = models.CharField(max_length=150)
    hospital_id = models.CharField(max_length=50)
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


# Pain Questions
class PainQuestions(models.Model):

    questions = models.CharField(max_length=255)

    class Meta:
        db_table = "pain_questions"


# Pain Answers
class PainAnswers(models.Model):

    answers = models.CharField(max_length=255)

    class Meta:
        db_table = "pain_answers"


# Pain Selection
class PainSelection(models.Model):
    patient_fk = models.ForeignKey(PatientRegister, on_delete=models.CASCADE)
    question_fk = models.ForeignKey(PainQuestions, on_delete=models.CASCADE)
    answer_fk = models.ForeignKey(PainAnswers, on_delete=models.CASCADE)
    key = models.BooleanField(default=False)
    comments = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = "pain_selection"


# Pain Details
class PainDetails(models.Model):
    patient_fk = models.ForeignKey(PatientRegister, on_delete=models.CASCADE)
    year_pain_began = models.CharField(max_length=20, blank=True, null=True)
    onset_of_pain = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=20)
    comments = models.TextField(blank=True)

    class Meta:
        db_table = "pain_details"
