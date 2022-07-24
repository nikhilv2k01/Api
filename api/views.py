import json
from django.forms import model_to_dict
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from .models import *
from .serializers import *
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


# Create your views here.


# Patient Register
@api_view(['POST'])
def patient_register(request):

    patient_data = JSONParser().parse(request)
    patient_serializer = PatientRegSerializer(data=patient_data)

    queryset = PatientRegister.objects.filter(
        Q(username=patient_data['username']) | Q(email=patient_data['email']))

    password1 = patient_data['password1']
    password2 = patient_data['password2']
    username = patient_data['username']
    email = patient_data['email']

    data = {}
    if patient_serializer.is_valid():
        if not queryset:
            if password1 == password2:
                user = User.objects.create_user(
                    username=username, email=email, password=password1)
                user.save()
                
                patient_serializer.auth_user_id = user.id
                auth = patient_serializer.auth_user_id
                print("hdgadgdgdgdg",auth)
                # obj = User.objects.get(username=username)
                # auth = obj.id
                # print("adsfadfadfdfdad",auth)
                
                # patient_serializer = auth
                patient_serializer.save()

                token = Token.objects.create(user=user)
                data['message'] = 'success'
                data['token'] = token.key

                return JsonResponse(data)

            else:
                return JsonResponse({'message': 'Password does not match'})
        else:
            return JsonResponse({'message': 'Email or Username already exist'})

    return JsonResponse(patient_serializer.errors)


# Patient Login
@api_view(['POST'])
def patient_login(request):

    patient_data = JSONParser().parse(request)
    patient_serializer = PatientLoginSerializer(data=patient_data)

    user_name = patient_data['username']
    password = patient_data['password1']

    if '@' in user_name:
        user_exist = PatientRegister.objects.filter(
            email=user_name, password1=password).exists()

    else:
        user_exist = PatientRegister.objects.filter(
            username=user_name, password1=password).exists()

    if '@' in user_name:
        data = PatientRegister.objects.get(
            email=user_name, password1=password).patient_id
    else:
        data = PatientRegister.objects.get(
            username=user_name, password1=password).patient_id

    if patient_serializer.is_valid():
        if user_exist:
            if data:
                return JsonResponse({'message': 'success', 'id': data})
                # return Response(data)
            # return JsonResponse({'message':'success'})
        else:
            return JsonResponse({'message': 'Please enter a vaild details'})
    return JsonResponse(patient_serializer.errors)


# Patient Display and Update
@api_view(['GET', 'PUT'])
def patient_display_update(request, id):

    if request.method == 'GET':
        querySet = PatientRegister.objects.get(patient_id=id)
        data = {}
        print(request.user)
        if querySet:
            data = model_to_dict(querySet, fields=[
                'patient_id', 'firstname', 'lastname', 'phone_number', 'email', 'hospital_number', 'dateofbirth', 'address', 'postcode'])
        return Response(data)

    else:
        patient_data = PatientRegister.objects.get(
            patient_id=id)
        patient_serializer = PatientUpdateSerializer(
            instance=patient_data, data=request.data)
        if patient_serializer.is_valid():
            patient_serializer.save()
            return JsonResponse(patient_serializer.data)
        return JsonResponse(patient_serializer.errors)


# Tech Support Register
@api_view(['POST'])
def tech_register(request):

    tech_data = JSONParser().parse(request)
    tech_serializer = TechRegSerializer(data=tech_data)

    queryset = TechRegister.objects.filter(
        Q(username=tech_data['username']) | Q(email=tech_data['email']))

    password1 = tech_data['password1']
    password2 = tech_data['password2']

    if tech_serializer.is_valid():
        if not queryset:
            if password1 == password2:
                tech_serializer.save()
                return JsonResponse({'message': 'Registered successfully'})
            else:
                return JsonResponse({'message': 'Password does not match'})
        else:
            return JsonResponse({'message': 'Email or Username already exist'})

    return JsonResponse(tech_serializer.errors)


# Tech Support Login
@api_view(['POST'])
def tech_login(request):

    tech_data = JSONParser().parse(request)
    tech_serializer = TechLoginSerializer(data=tech_data)

    user_name = tech_data['username']
    password = tech_data['password1']

    if '@' in user_name:
        user_exist = TechRegister.objects.filter(
            email=user_name, password1=password).exists()

    else:
        user_exist = TechRegister.objects.filter(
            username=user_name, password1=password).exists()

    if tech_serializer.is_valid():
        if user_exist:
            return JsonResponse({'message': 'Success'})
        else:
            return JsonResponse({'message': 'Please enter a vaild details'})
    return JsonResponse(tech_serializer.errors)


# Tech Details Display
@api_view(['GET'])
def tech_display(request):
    tech_data = TechRegister.objects.all()
    json_data = [{'id': i.tech_id, 'name': i.name, 'username': i.username,
                  'email': i.email, 'phone_number': i.phone_number, 'address': i.address, 'password1': i.password1, 'password2': i.password2, }for i in tech_data]
    return JsonResponse({'message': json_data})


# Doctor Register
@api_view(['POST'])
def doctor_register(request):

    doctor_data = JSONParser().parse(request)
    doctor_serializer = DoctorRegSerializer(data=doctor_data)

    queryset = DoctorRegister.objects.filter(
        Q(username=doctor_data['username']) | Q(email=doctor_data['email']))

    password1 = doctor_data['password1']
    password2 = doctor_data['password2']

    if doctor_serializer.is_valid():
        if not queryset:
            if password1 == password2:
                doctor_serializer.save()
                return JsonResponse({'message': ' Registered successfully'})
            else:
                return JsonResponse({'message': 'Password does not match'})
        else:
            return JsonResponse({'message': 'Email or Username already exist'})

    return JsonResponse(doctor_serializer.errors)


# Doctor Login
@api_view(['POST'])
def doctor_login(request):

    doctor_data = JSONParser().parse(request)
    doctor_serializer = DoctorLoginSerializer(data=doctor_data)

    user_name = doctor_data['username']
    password = doctor_data['password1']

    if '@' in user_name:
        user_exist = DoctorRegister.objects.filter(
            email=user_name, password1=password).exists()

    else:
        user_exist = DoctorRegister.objects.filter(
            username=user_name, password1=password).exists()

    if doctor_serializer.is_valid():
        if user_exist:
            return JsonResponse({'message': 'Success'})
        else:
            return JsonResponse({'message': 'Please enter a vaild details'})
    return JsonResponse(doctor_serializer.errors)


# Doctor Details Display
@api_view(['GET'])
def doctor_display(request):
    doctor_data = DoctorRegister.objects.all()
    json_data = [{'id': i.doctor_id, 'name': i.name, 'username': i.username,
                  'email': i.email, 'phone_number': i.phone_number, 'hospital_address': i.hospital_address, 'password1': i.password1, 'password2': i.password2, }for i in doctor_data]
    return JsonResponse({'message': json_data})


# Pain Details
@api_view(['POST'])
def pain_details(request):

    details_data = JSONParser().parse(request)
    details_serializer = PainDetailsSerializer(data=details_data)

    if request.method == 'POST':

        if details_serializer.is_valid():
            details_serializer.save()
            return JsonResponse({'message': details_data})
        return JsonResponse(details_serializer.errors)


# Pain Start
@api_view(['POST'])
def pain_start(request):
    start_data = JSONParser().parse(request)
    start_serializer = PainStartSerializer(data=start_data)

    if start_serializer.is_valid():
        start_serializer.save()
        return JsonResponse({'message': start_data})
    return JsonResponse(start_serializer.errors)


# Pain Type
@api_view(['POST'])
def pain_type(request):
    type_data = JSONParser().parse(request)
    type_serializer = PainTypeSerializer(data=type_data)

    if type_serializer.is_valid():
        type_serializer.save()
        return JsonResponse({'message': type_data})
    return JsonResponse(type_serializer.errors)
