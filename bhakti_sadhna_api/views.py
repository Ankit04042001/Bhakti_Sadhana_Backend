from .models import User, Attendence, Task, Otp
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsAdminOrReadOnly
from django.views import View
import uuid, datetime
from django.core.mail import send_mail
import os
from smtplib import SMTPException
from django.contrib.auth import logout





#******************** User Registeration View *********************/

class RegisterUserAPIView(generics.GenericAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]
    

    def post(self, request):
        otp = str(int(uuid.uuid1()))[:6]
        serializer = self.serializer_class(data = request.data, context={'request' : request, 'otp' : otp})
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        request.session['email'] = email
        try:
            send_mail(
                'Register Account',
                'Otp for your registeration is ' + otp,
                os.environ.get('EMAIL_HOST_USER',''),
                [email],
                fail_silently=False,
                )

        except SMTPException as e:
            return Response({"status" : False, "message" : str(e)})
    
        return Response({
            "status" : True,
            "message" : "Otp sent successfully.",
            "data" : {
                
            }
        })

#******************** End of Registeration View *********************/

#******************** Otp Validation View for User Registeration *********************/

class ValidateOtpForRegisterationAPIView(generics.GenericAPIView):
    serializer_class = ValidateOtpForRegisterationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request' : request})
        serializer.is_valid(raise_exception=True)
        otp_model = Otp.objects.get(email=request.session.get('email'))
        user = otp_model.email
        first_name = otp_model.first_name
        last_name = otp_model.last_name

        del request.session['email']
        otp_model.delete()

        return Response({
            "status" : True,
            "message":"registeration successful",
            "data" : {
                "user" : user, 
                "first_name" : first_name,
                "last_name" : last_name
            }
        })  
        
#******************** End of Otp Validation View *********************/

# #******************** Login View *********************/

class LoginAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    
    def post(self, request):
        
        serializer = self.serializer_class(data=request.data, context={'request' : request})
        serializer.is_valid(raise_exception = True)

    
        return Response({
            "status" : True,
            "message" : "login successful", 
            "data" : {
                "user" : request.user.email, 
                "first_name" : request.user.first_name
            }
        })
    

# #******************** End of Login View *********************/



#******************** Password change view while logged in  *********************/

class ChangePasswordAPIView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context = {'request':request})
        serializer.is_valid(raise_exception=True)

        return Response({
            "status" : True,
            "message" : "Password Changed Successfully.",
            "data" : {

            }
            })


#******************** End of password change View *********************/


#******************** Logout View *********************/

class LogoutAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request) 
        
        return Response({
            "status" : True,
            "message" : "Logged Out Successfully.",
            "data" : {
                
            }
            })       
#******************** End of Logout View *********************/

#******************** Forget Password View *********************/

class ForgetPasswordAPIView(generics.GenericAPIView):
    serializer_class = ForgetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        try:
            user = User.objects.get(email=email)
        except:
            return Response({
                "status" : False,
                "message" : "User with this email id doesn't exist."
            })
        otp = str(int(uuid.uuid1()))[:6]
        try:
            otp_model = Otp.objects.get(email=email)
            otp_model.delete()
        except:
            pass
        otp_model = Otp(email=user.email, otp=otp)
        otp_model.save()

        request.session['email'] = email
        try:
            send_mail(
                'Reset Account',
                'Otp for reseting your password is ' + otp,
                os.environ.get('EMAIL_HOST_USER',''),
                [email],
                fail_silently=False,
                )
        except Exception as e:
            return Response({
                "status" : False,
                "message" : str(e)
                })
        return Response({
            "status" : True,
            "message" : "Otp Sent Successfully",
            "data" : {
                
            }
        })


#******************** End of Forget Password View *********************/


#******************** Otp Validation View for forget Password *********************/

class ValidateOtpForForgetPasswordAPIView(generics.GenericAPIView):
    serializer_class = ValidateOtpForForgetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        otp_model = Otp.objects.get(email=request.session.get('email'))
        otp_model.delete()
        del request.session['email']
        return Response({
            "status" : True,
            "message":"Password Reset success.",
            "data" : {
                
            }
        })    

#******************** End of Forget Password View *********************/



#******************** Get User View *********************/

class GetUserAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "status" : True,
            "message" : "User fetched Successfully",
            "data" : {
                "first_name" : request.user.first_name
            }
        })


#******************** End of Get User View *********************/

#******************** Handling Attendence, punch in, punch out *********************/

class AttendenceListAPIView(generics.GenericAPIView):
    serializer_class = AttendenceSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        attendence = Attendence.objects.all().filter(user=request.user.id, date=datetime.date.today())
        import pdb
        pdb.set_trace
        serializer = self.serializer_class(attendence, many=True)
        return Response({
            "status" : True, 
            "data" : {
                "date" : str(attendence[0].date),
                "punch in" : attendence[0].punch_in,
                "user" : attendence[0].user.email,
                "first_name" : attendence[0].user.first_name,
                "last_name" : attendence[0].user.last_name,
                "attendence status" : attendence[0].attendence_status
            }
            })

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            attendence = Attendence.objects.get(user=request.user.id)
        except:
            return Response({
                "status" : False,
                "message" : "No Detail Found"
            })

        if serializer.data['date'] == str(datetime.date.today()) and attendence.attendence_status == 'A' and serializer.data['punch_status'] == True:
            attendence.attendence_status = 'P'
            attendence.punch_in = datetime.datetime.now().strftime("%H:%M:%S")
            attendence.save()
            return Response({
                "status" : True, 
                "data" : {
                    "date" : str(attendence.date),
                    "punch in" : attendence.punch_in,
                    "user" : attendence.user.email,
                    "first_name" : attendence.user.first_name,
                    "last_name" : attendence.user.last_name,
                    "attendence status" : attendence.attendence_status
                }
            })
        

        if serializer.data['date'] == str(datetime.date.today()) and attendence.attendence_status == 'P' and serializer.data['punch_status'] == True:
            return Response({
                "status" : False, 
                "message" : "Attendence Already Marked"
            })

        else :
            return Response({
                "status" : True, 
                "data" : {
                    "date" : str(attendence.date),
                    "punch in" : attendence.punch_in,
                    "user" : attendence.user.email,
                    "first_name" : attendence.user.first_name,
                    "last_name" : attendence.user.last_name,
                    "attendence status" : attendence.attendence_status
                }   
            })

    
#******************** End of Atttendenc View *********************/



#******************** Task View *********************/

class TaskListAPIView(generics.GenericAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        data = Task.objects.all()
        return Response({
            "status" : True,
            "data" : list(self.queryset.values())
        })

#******************** End of Task View *********************/
