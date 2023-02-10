from django.urls import path, include
from .views import (
                   RegisterUserAPIView,
                   ValidateOtpForRegisterationAPIView,
                   LoginAPIView,
                   ChangePasswordAPIView,
                   LogoutAPIView,
                   ForgetPasswordAPIView,
                   ValidateOtpForForgetPasswordAPIView,
                   GetUserAPIView,
                   AttendenceListAPIView,
                   TaskListAPIView
                   )




urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('reg_otp/', ValidateOtpForRegisterationAPIView.as_view(), name='r_otp'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('get_user/', GetUserAPIView.as_view(), name='get_user'),
    path('change_password/', ChangePasswordAPIView.as_view(), name='change_password'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('reset_password/', ForgetPasswordAPIView.as_view(), name='reset_password'),
    path('reset_otp/', ValidateOtpForForgetPasswordAPIView.as_view(), name='reset_otp'),
    path('attendence/', AttendenceListAPIView.as_view(), name='attendence'),
    path('task/', TaskListAPIView.as_view(), name='task')
]
