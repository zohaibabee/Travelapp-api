from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from django.core.mail import send_mail
from rest_framework.response import Response
from .serializer import Registrationserailizer,Verifyotpserializer,Loginserializer,Changepasswordserializer,Sendemailserializer,Resetpasswordserializer
from django.conf import settings
import random
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .utils import Util

# Create your views here.
from rest_framework import status
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class Registration(APIView):
    def post(self,request):
        serializer=Registrationserailizer(data=request.data)
        if serializer.is_valid():
            email=serializer.validated_data['email']
            password=serializer.validated_data['password']  # Fixed typo, changed () to []
            name=serializer.validated_data['name']
            otp=random.randint(1000,9999)
            print(otp)
            user=User.objects.create_user(email=email,password=password,name=name,otp=otp)
            data={
                'subject':'Reset Password Link',
                'body':f'This is your one time password {otp}',
                'to_email':[email]
            }
            Util.send_email(data)
            
            return Response({'msg':'check your email'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            
            

class Verifyotp(APIView):
    def post(self, request):
        serializer = Verifyotpserializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Save changes to the user object
            return Response({'msg': 'OTP verified'})
        return Response(serializer.errors)
    
    

class Login(APIView):
    def post(self,request):
        serializer=Loginserializer(data=request.data)
        if serializer.is_valid():
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            if not User.objects.filter(email=email, is_verified=True).exists():
                return Response({'msg': 'Please verify your OTP'}, status=status.HTTP_400_BAD_REQUEST)
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'token':token,'msg':'login success'},status=status.HTTP_200_OK)
            else:
                return Response({'msg':'email or password is invalid'},status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)   
    
    

class Changepassword(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer=Changepasswordserializer(data=request.data,context={'user':request.user})
        if serializer.is_valid():
            return Response({'msg':'Password change'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 

class Sendemail(APIView):
    def post(self,request):
        serializer=Sendemailserializer(data=request.data)
        if serializer.is_valid():
            return Response({'msg':'Link send to your email chack the email'})
        return Response(serializer.errors)
    
    
class Resetpassword(APIView):
    def post(self,request,uid,token):
        serializer=Resetpasswordserializer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid():
            return Response({'msg':'password reset successfully'})
        return Response(serializer.errors)