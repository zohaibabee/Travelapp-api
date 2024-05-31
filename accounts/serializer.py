from .models import User
from rest_framework import serializers
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from accounts.utils import OtpHandler


class Registrationserailizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'otp': {'read_only': True}
        }

    def create(self, validated_data):
        email = validated_data['email']
        name = validated_data['name']
        password = validated_data['password']
        user = User.objects.create_user(
            email=email, name=name, password=password)
        return user


class ResendOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')

        # Check if user exists with the given email
        user_exists = User.objects.filter(email=email).exists()
        if not user_exists:
            raise serializers.ValidationError(
                'Your account is not registered.')

        # Retrieve the user object
        user = User.objects.get(email=email)
        attrs['user'] = user
        return attrs


class Verifyotpserializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')

        # Check if user exists with the given email
        user_exists = User.objects.filter(email=email).exists()
        if not user_exists:
            raise serializers.ValidationError(
                'Your account is not registered.')

        # Retrieve the user object
        user = User.objects.get(email=email)

        # Check if OTP matches
        status, msg = OtpHandler.verify_otp(user, otp)
        if status == -1:
            raise serializers.ValidationError(msg)

        # Mark user as verified
        user.is_active = True
        user.save()
        return attrs



class Changepasswordserializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            return serializers.ValidationError('password is not match')
        user.set_password(password)
        user.save()

        return attrs


class Sendemailserializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            # print(user)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            passwordtoken = PasswordResetTokenGenerator().make_token(user)
            link = 'http://localhost:300/user/reset/'+uid+'/'+passwordtoken
            print(link)
            # data={
            #     'subject':'Reset Password Link',
            #     'body':'Click on link to reset the password'+link,
            #     'to_email':[user]
            # }
            # Util.send_email(data)

        else:
            raise serializers.ValidationError('user is not register')
        return attrs


class Resetpasswordserializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        uid = self.context.get('uid')
        token = self.context.get('token')
        if password != password2:
            raise serializers.ValidationError('Passwords do not match')
        id = urlsafe_base64_decode(smart_str(uid))
        user = User.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError('TOken is not valid or Expire')
        user.set_password(password)
        user.save()
        return attrs
