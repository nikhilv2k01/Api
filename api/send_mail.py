
from django.core.mail import send_mail
from django.conf import settings


# Forget password
def send_forget_password_mail(email, reset_link):

    subject = 'Your forget password link'
    message = f'Hi click on the link to reset your password {reset_link}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True


# Email verification
def send_email_verification_mail(email, verify_link):

    subject = 'Your accounts need to be verified'
    message = f'Hi click on the  link to verify your account {verify_link}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True