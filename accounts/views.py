from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from .serializer import ResendOtpSerializer, Registrationserailizer, Verifyotpserializer, Changepasswordserializer, Sendemailserializer, Resetpasswordserializer
from rest_framework.permissions import IsAuthenticated
from .utils import OtpHandler

# Create your views here.
from rest_framework import status


class Registration(CreateAPIView):
    serializer_class = Registrationserailizer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                OtpHandler.send_and_store_otp(user)
                return Response({'msg': 'OTP sent to your email'}, status=status.HTTP_201_CREATED)


class ResendOtp(CreateAPIView):
    serializer_class = ResendOtpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            OtpHandler.send_and_store_otp(user)
            return Response({'msg': 'OTP sent to your email'}, status=status.HTTP_200_OK)


class Verifyotp(GenericAPIView):
    serializer_class = Verifyotpserializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'OTP verified'})
        return Response(serializer.errors)


class Changepassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Changepasswordserializer(
            data=request.data, context={'user': request.user})
        if serializer.is_valid():
            return Response({'msg': 'Password change'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Sendemail(APIView):
    def post(self, request):
        serializer = Sendemailserializer(data=request.data)
        if serializer.is_valid():
            return Response({'msg': 'Link send to your email chack the email'})
        return Response(serializer.errors)


class Resetpassword(APIView):
    def post(self, request, uid, token):
        serializer = Resetpasswordserializer(data=request.data, context={
                                             'uid': uid, 'token': token})
        if serializer.is_valid():
            return Response({'msg': 'password reset successfully'})
        return Response(serializer.errors)
