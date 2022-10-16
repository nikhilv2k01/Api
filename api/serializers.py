from rest_framework import serializers
from .models import *

from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode


# Patient Register Serializer
class PatientRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientRegister
        fields = ['firstname', 'lastname', 'username',
                  'email', 'phone_number', 'password1', 'password2']


# Patient Login Serializer
class PatientLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientRegister
        fields = ['username', 'password1', 'time_stamp']


# Change password serializer
class PatientChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientRegister
        fields = ['password1', 'password2']

    def validate(self, data):
        """
        Verify token and encoded_pk and then set new password.
        """
        newpassword = data.get("password1")
        confirmpassword = data.get("password2")
        token = self.context.get("kwargs").get("token")
        encoded_pk = self.context.get("kwargs").get("encoded_pk")

        if token is None or encoded_pk is None:
            raise serializers.ValidationError("Missing data.")

        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = User.objects.get(pk=pk)
        patient = PatientRegister.objects.filter(patient_id=pk).first()
        check_token = PasswordResetTokenGenerator().check_token(user, token)
        print("check_token",check_token)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The reset token is invalid")
        else:
            if newpassword != confirmpassword:
                raise serializers.ValidationError("Password does not match")
            else:
                user.set_password(newpassword)
                user.save()
                patient.password1 = newpassword
                patient.password2 = confirmpassword
                patient.save()
        return data


# Forget Password serializer
class PatientForgetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientRegister
        fields = ['email']


# Patient Update Serializer
class PatientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientRegister
        fields = ['firstname', 'lastname',  'phone_number', 'dateofbirth',
                  'email', 'hospital_number', 'address', 'postcode']


# Tech Support Register Serializer
class TechRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechRegister
        fields = ['name', 'username', 'email', 'phone_number',
                  'address', 'password1', 'password2']


# Tech Support Login Serializer
class TechLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechRegister
        fields = ['username', 'password1']


# Doctor Register Serializer
class DoctorRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorRegister
        fields = ['firstname', 'lastname', 'username',
                  'specialization', 'hospital_id', 'email', 'phone_number', 'password1', 'password2']


# Doctor Login Serializer
class DoctorLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorRegister
        fields = ['username', 'password1']


# Pain Details Serializer
class PainDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PainDetails
        fields = ['year_pain_began', 'onset_of_pain', 'gender', 'comments']
