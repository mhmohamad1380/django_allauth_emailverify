from time import sleep
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def sending_verification_email(email,token):
    send_mail("Account Verification",f"http://localhost:8000/user?email_verify={token}",'from@madmail.com',[email])
