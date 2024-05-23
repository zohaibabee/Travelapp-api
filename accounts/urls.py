from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.Registration.as_view()),
    path('verifyotp/',views.Verifyotp.as_view()),
    path('login/',views.Login.as_view()),
    path('changepass/',views.Changepassword.as_view()),
    path('sendemail/',views.Sendemail.as_view()),
    path('resetpassword/<str:uid>/<str:token>/',views.Resetpassword.as_view()),
    
]