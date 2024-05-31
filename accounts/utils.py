import random
from datetime import timedelta
from django.utils import timezone
from django.core.mail import EmailMessage
from django.contrib.auth.hashers import check_password
from accounts.models import OTP
import os

class EmailHandler:
    @staticmethod
    def send_email(data):
        email=EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=os.environ.get('EMAIL_FROM'),
            to=data['to_email']
        )
        email.send()

class OtpHandler:
    @staticmethod
    def generate_otp():
        return random.randint(1000,9999)

    @staticmethod
    def send_and_store_otp(user):
        otp = OtpHandler.generate_otp()
        print(f'OTP for {user.email} is {otp}')
        data={
            'subject':'Confirm your email address for Nomadic Tours',
            'body':'Your OTP is '+ str(otp),
            'to_email':[user.email]
        }
        # EmailHandler.send_email(data)
        OTP.objects.create(user=user, otp=str(otp))
    
    @staticmethod
    def verify_otp(user, otp):
        otp_obj = OTP.objects.filter(user=user).order_by('-created_at').first()
        if otp_obj.created_at < timezone.now() - timedelta(minutes=5):
            return -1, "OTP expired. Please request a new OTP."

        if check_password(otp, otp_obj.otp):
            return 1, "OTP verified"
        return -1, "Invalid OTP. Please try again."
        