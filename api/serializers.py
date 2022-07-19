from rest_framework import serializers
from .models import *


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
        fields = ['username', 'password1']


# Patient Update Serializer
class PatientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientRegister
        fields = ['firstname', 'lastname',  'phone_number',
                  'email', 'hospital_number', 'dateofbirth', 'address', 'postcode']


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
        fields = ['name', 'username', 'email', 'phone_number',
                  'hospital_address', 'password1', 'password2']


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


# Pain Start Serializer
class PainStartSerializer(serializers.ModelSerializer):
    class Meta:
        model = PainStartTable
        fields = ['accident_at_work', 'accident_at_home', 'following_illness',
                  'following_surgery', 'road_traffic_accident', 'pain_just_began', 'others']


# Pain Type Serializer
class PainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PainTypeTable
        fields = ['throbbing', 'shooting', 'stabbing',
                  'sharp', 'cramping', 'gnawing', 'hot_burning', 'aching', 'heavy', 'tender', 'splitting', 'tiring_exhausting', 'sickening', 'fearful', 'pushing_cruel']
