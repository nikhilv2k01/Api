from ast import Return
from email import message
from select import select
from django.forms import model_to_dict
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from .models import *
from .serializers import *
from django.db.models import Q
from rest_framework.response import Response

from datetime import datetime

from .send_mail import send_email_verification_mail, send_forget_password_mail

from rest_framework import generics, status, response

from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

import jwt
import datetime


# Create your views here.


# Patient Register
@api_view(['POST'])
def patient_register(request):
    print("python register")
    patient_data = JSONParser().parse(request)
    patient_serializer = PatientRegSerializer(data=patient_data)

    user_exist = PatientRegister.objects.filter(
        username=patient_data['username'])
    email_exist = PatientRegister.objects.filter(email=patient_data['email'])

    email = patient_data['email']
    username = patient_data['username']
    password1 = patient_data['password1']
    password2 = patient_data['password2']

    # user = User.objects.filter(email=email).first()
    try:

        if patient_serializer.is_valid():

            if user_exist:
                return JsonResponse({'message': 'Username already exist'})

            if email_exist:
                return JsonResponse({'message': 'Email already exist'})

            if password1 == password2:

                user = User.objects.create_user(
                    username=username, email=email, password=password1)
                user.save()

                payload = {
                    'id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    'iat': datetime.datetime.utcnow()
                }
                auth_token = jwt.encode(payload, 'secret', algorithm='HS256')
                patient_serializer.save(auth_token=auth_token)

                verify_link = f'http://localhost:3000/verify/{auth_token}'

                send_email_verification_mail(email, verify_link)

                data = [patient_serializer.data]
                response = Response()
                response.set_cookie(key='jwt', value=auth_token, httponly=True)
                response.data = {
                    "status": True,
                    "status_code": status.HTTP_200_OK,
                    "message": "success",
                    "auth_token": auth_token,
                    "data": data,
                }
                return response

            else:
                return JsonResponse({'message': 'Password does not match'})

        return JsonResponse(patient_serializer.errors)

    except Exception as e:
        print(e)


# Patient Login
@api_view(['POST'])
def patient_login(request):

    patient_data = JSONParser().parse(request)
    patient_serializer = PatientLoginSerializer(data=patient_data)

    user_name = patient_data['username']
    password = patient_data['password1']

    if '@' in user_name:
        user_exist = PatientRegister.objects.filter(
            email=user_name, password1=password).first()

    else:
        user_exist = PatientRegister.objects.filter(
            username=user_name, password1=password).first()

    if patient_serializer.is_valid():
        if user_exist:
            if not user_exist.is_verified:
                return JsonResponse({
                    "message": "Your account is not verified check your mail."
                })
            current_datetime = datetime.datetime.now()

            patient_serializer.time_stamp = current_datetime
            time_stamp = patient_serializer.time_stamp
            PatientRegister.objects.filter(
                username=user_name).update(time_stamp=time_stamp)

            if '@' in user_name:
                id = PatientRegister.objects.filter(
                    email=user_name, password1=password).first()
            else:
                id = PatientRegister.objects.filter(
                    username=user_name, password1=password).first()

            user_id = id.patient_id
            data = [patient_serializer.data]
            return JsonResponse({
                'status': True,
                'status_code': status.HTTP_200_OK,
                'message': 'success',
                'id': user_id,
                'data': data,
            })

        else:
            return JsonResponse({'message': 'Please enter a vaild details'})
    return JsonResponse(patient_serializer.errors)


# Patient Display
@api_view(['GET'])
def patient_display(request, id):

    querySet = PatientRegister.objects.get(patient_id=id)
    data = {}

    if querySet:
        data = model_to_dict(querySet, fields=[
            'patient_id', 'firstname', 'lastname', 'phone_number', 'email', 'hospital_number', 'dateofbirth', 'address', 'postcode'])
    return Response(data)


# Patient Update
@api_view(['PUT'])
def patient_update(request, id):

    patient_data = PatientRegister.objects.get(
        patient_id=id)
    patient_serializer = PatientUpdateSerializer(
        instance=patient_data, data=request.data)

    queryset = PatientRegister.objects.filter(email=request.data['email'])

    if patient_serializer.is_valid():
        if not queryset:
            patient_serializer.save()
        elif patient_serializer.is_valid():
            if patient_data.email == request.data['email']:
                patient_serializer.save()
            else:
                return JsonResponse({"message": "email already exists"})
        return JsonResponse(patient_serializer.data)

    return JsonResponse(patient_serializer.errors)


# forget password link creating
class PasswordReset(generics.GenericAPIView):
    """
    Request for Password Reset Link.
    """

    serializer_class = PatientForgetPasswordSerializer

    def post(self, request):
        """
        Create token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = User.objects.filter(email=email).first()
        try:

            if user:
                encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
                token = PasswordResetTokenGenerator().make_token(user)

                reset_url = reverse(
                    "reset-password",
                    kwargs={"encoded_pk": encoded_pk, "token": token},
                )
                print("password token", reset_url)
                reset_link = f"http://localhost:3000/ChangePassword{reset_url}"
                send_email = PatientRegister.objects.get(email=email).email

                send_forget_password_mail(send_email, reset_link)

                return response.Response(
                    {
                        "message": "success",
                        "encoded_pk": encoded_pk,
                        "token": token
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return response.Response(
                    {
                        "message": "User doesn't exists"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            print(e)


# Changing Password
class ChangePassword(generics.GenericAPIView):
    """
    Verify and Reset Password Token View.
    """

    serializer_class = PatientChangePasswordSerializer

    def patch(self, request, *args, **kwargs):
        """
        Verify token & encoded_pk and then reset the password.
        """
        serializer = self.serializer_class(
            data=request.data, context={"kwargs": kwargs}
        )
        if serializer.is_valid(raise_exception=True):
            return response.Response(
                {
                    "message": "success"
                },
                status=status.HTTP_200_OK,
            )
        else:
            return response.Response(serializer.errors)


# Email verification
@api_view(['POST'])
def verify(request, auth_token):

    try:
        patient_obj = PatientRegister.objects.filter(
            auth_token=auth_token).first()
        if patient_obj:
            if patient_obj.is_verified:
                return response.Response(
                    {
                        "message": "Your account is already verified."
                    }
                )
            patient_obj.is_verified = True
            patient_obj.save()
            return response.Response(
                {
                    "message": "Your account has been verified.",
                },
                status=status.HTTP_200_OK,
            )

        else:
            return response.Response(
                {
                    "message": "Link is invalid or expired"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
    except Exception as e:
        print(e)


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
                return JsonResponse({'message': 'success'})
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


# Pain Questions
@api_view(['POST'])
def pain_selection(request, id):
    selection_data = JSONParser().parse(request)

    question_selection = selection_data.keys()

    pain_Start = selection_data['pain_start']
    discribe_pain = selection_data['discribe_pain']

    print("questions = ", question_selection)

    print('pain start = ', pain_Start)
    print('discribe pain = ', discribe_pain)

    update = PainSelection.objects.filter(patient_fk=id)
    for upd in update:

        PainSelection.objects.filter(
            patient_fk=id).update(key=False)
        print("updated user key to false")

    for i in question_selection:  # questions
        print("questions", i)

        if i == "pain_start":
            print("yes pain start")

            for start in pain_Start:

                pain_start_answers = PainAnswers.objects.filter(answers=start)
                patient_fk = id

                if pain_start_answers:

                    print("yes answers of pain_start", start)
                    question_obj = PainQuestions.objects.get(questions=i)
                    answer_obj = PainAnswers.objects.get(answers=start)
                    question_fk = question_obj.id
                    answer_fk = answer_obj.id
                    key = True
                    current_datetime = datetime.datetime.now()

                    check_exist = PainSelection.objects.filter(
                        patient_fk=patient_fk, question_fk=question_fk, answer_fk=answer_fk)

                    if check_exist:
                        print("check exist is true")
                        for check in check_exist:
                            print("check id = ", check.id)
                            PainSelection.objects.filter(
                                patient_fk=patient_fk, question_fk=question_fk, answer_fk=answer_fk).update(key=False)
                            print("updated key to false")

                    pain_selection = PainSelection(
                        patient_fk_id=patient_fk, question_fk_id=question_fk, answer_fk_id=answer_fk, key=key, time_stamp=current_datetime)

                    pain_selection.save()
                    print("saved.....")
                else:
                    print("not pain start")
                    return JsonResponse({"message": "Answers does not match"})

        if i == "discribe_pain":
            print("yes discribe pain")

            for discribe in discribe_pain:
                discribe_pain_answers = PainAnswers.objects.filter(
                    answers=discribe)
                patient_fk = id

                if discribe_pain_answers:
                    print("yes answers of pain_now ", discribe)
                    question_obj = PainQuestions.objects.get(questions=i)
                    answer_obj = PainAnswers.objects.get(answers=discribe)
                    question_fk = question_obj.id
                    answer_fk = answer_obj.id
                    key = True
                    current_datetime = datetime.datetime.now()

                    check_exist = PainSelection.objects.filter(
                        patient_fk=patient_fk, question_fk=question_fk, answer_fk=answer_fk)

                    if check_exist:
                        print("check exist is true")
                        for check in check_exist:
                            print("check id = ", check.id)
                            PainSelection.objects.filter(
                                patient_fk=patient_fk, question_fk=question_fk, answer_fk=answer_fk).update(key=False)
                            print("updated key to false")

                    pain_selection = PainSelection(
                        patient_fk_id=patient_fk, question_fk_id=question_fk, answer_fk_id=answer_fk, key=key, time_stamp=current_datetime)
                    pain_selection.save()
                    print("saved.....")

                else:
                    print("not discribe pain")
                    return JsonResponse({"message": "Answers does not match"})
        else:
            print("not discribe pain")

    return JsonResponse({
        'status': True,
        'status_code': status.HTTP_200_OK,
        'message': 'success',

    })


# Pain details
@api_view(['POST'])
def pain_details(request, id):

    details_data = JSONParser().parse(request)
    serializer = PainDetailsSerializer(data=details_data)
    obj = PainDetails.objects.filter(patient_fk=id).first()
    year_pain_began = details_data['year_pain_began']
    onset_of_pain = details_data['onset_of_pain']
    gender = details_data['gender']
    comments = details_data['comments']

    if serializer.is_valid():
        if not obj:
            serializer.patient_fk_id = id
            fk = serializer.patient_fk_id
            serializer.save(patient_fk_id=fk)

            return JsonResponse({
                'status': True,
                'status_code': status.HTTP_200_OK,
                'message': 'success',
            })

        else:
            PainDetails.objects.filter(patient_fk=id).update(
                year_pain_began=year_pain_began, onset_of_pain=onset_of_pain, gender=gender, comments=comments)
            return JsonResponse({
                'status': True,
                'status_code': status.HTTP_200_OK,
                'message': 'success',
            })
    return JsonResponse(serializer.errors)


# Pain Details display

@api_view(['GET'])
def pain_details_display(request, id):

    pain_details = PainDetails.objects.filter(patient_fk=id).first()

    pain_start = PainQuestions.objects.filter(questions="pain_start").first()
    discribe_pain = PainQuestions.objects.filter(
        questions="discribe_pain").first()

    pain_start_selection = PainSelection.objects.filter(
        question_fk=pain_start.id, patient_fk=id, key=True)

    discribe_pain_selection = PainSelection.objects.filter(
        question_fk=discribe_pain.id, patient_fk=id, key=True)

    # Pain Start
    pain_start_dict = {}
    pain_start_data = []
    for i in pain_start_selection:
        print("pain start selection = ", i.answer_fk.answers)
        pain_start_dict['answers'] = i.answer_fk.answers
        pain_start_data.append(pain_start_dict['answers'])
    print("pain start = ", pain_start_data)

    # Discribe Pain
    discribe_pain_dict = {}
    discribe_pain_data = []
    for i in discribe_pain_selection:
        print("discribe pain selection = ", i.answer_fk.answers)
        discribe_pain_dict['answers'] = i.answer_fk.answers
        discribe_pain_data.append(discribe_pain_dict['answers'])
    print("discribe pain = ", discribe_pain_data)

    # Pain Details
    pain_details_data = {}
    if pain_details:
        pain_details_data = model_to_dict(
            pain_details, fields=['year_pain_began', 'onset_of_pain', 'gender', 'comments'])
    print("Pain Details = ", pain_details_data)

    return Response({
        'pain_details': pain_details_data,
        'pain_start': pain_start_data,
        'discribe_pain': discribe_pain_data
    })


@api_view(['PUT'])
def present_pain_pattern(request, id):

    # details_data = JSONParser().parse(request)
    # serializer = PresentPainPatternSerializer(data=details_data)
    obj = PainDetails.objects.get(patient_fk=id)
    serializer = PresentPainPatternSerializer(
        instance=obj, data=request.data)

    no_pain = request.data['no_pain']
    pain_free = request.data['pain_free']

    # often_pain = details_data['often_pain']
    # no_pain = details_data['no_pain']
    # pain_free = details_data['pain_free']
    # time_of_pain_best = details_data['time_of_pain_best']
    # time_of_pain_worst = details_data['time_of_pain_worst']
    # increase_pain_comments = details_data['increase_pain_comments']
    # decrease_pain_comments = details_data['decrease_pain_comments']
    # relieve_pain_comments = details_data['relieve_pain_comments']
    # trouble_sleep = details_data['trouble_sleep']
    # medication_sleep = details_data['medication_sleep']
    # awake_pain = details_data['awake_pain']
    # present_pain_comments = details_data['present_pain_comments']

    if serializer.is_valid():
        print("valid")

        if no_pain == 'No':
            pain_free = ""
        print("pain_free", pain_free)
        serializer.save(pain_free=pain_free)
        # PainDetails.objects.filter(patient_fk=id).update(
        #     often_pain=often_pain, no_pain=no_pain, pain_free=pain_free, time_of_pain_best=time_of_pain_best, time_of_pain_worst=time_of_pain_worst, increase_pain_comments=increase_pain_comments, decrease_pain_comments=decrease_pain_comments, relieve_pain_comments=relieve_pain_comments, trouble_sleep=trouble_sleep, medication_sleep=medication_sleep, awake_pain=awake_pain, present_pain_comments=present_pain_comments)
        print("updated")
        return JsonResponse({
            'status': True,
            'status_code': status.HTTP_200_OK,
            'message': 'success',
        })
