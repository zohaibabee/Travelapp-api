from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/',views.Registration.as_view()),
    path('verify-otp/',views.Verifyotp.as_view()),
    path('token/create/', TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('changepass/',views.Changepassword.as_view()),
    path('sendemail/',views.Sendemail.as_view()),
    path('resend-otp/',views.ResendOtp.as_view()),
    path('resetpassword/<str:uid>/<str:token>/',views.Resetpassword.as_view()),
]