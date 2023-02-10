from .models import User, Attendence, Task, Otp 
from rest_framework import serializers
from rest_framework import generics
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from datetime import datetime
from django.contrib.auth import authenticate, login



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name',)
        extra_kwargs = {'first_name':{'read_only':True}}


# ************ User Registration serializer ***************************************************#

class RegisterUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'})
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True, 'style':{'input_type':'password'}},'password2': {'write_only': True}, 'first_name' : {'required':True} }
        style = {'password':{'input_type':'password'}}

    def validate(self, attrs):
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')
        email = attrs.get('email')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        otp = self.context['otp']
        request = self.context['request']
        if first_name == '':
            raise serializers.ValidationError("First Name is required")
        if last_name == '':
            raise serializers.ValidationError("Last Name is required")
        if password and password2 and password != password2:
            raise serializers.ValidationError("Password and Confirm Password Doesn't match.")
        try:
            otp_model = Otp.objects.get(email=email)
            otp_model.delete()
        except:
            pass
        otp_model = Otp(first_name=first_name, last_name=last_name, email=email, password=make_password(password), otp=otp)
        otp_model.save()
        return attrs


#********************** otp validation for user registeration ******************************#

class ValidateOtpForRegisterationSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(max_length = 6)
    class Meta:
        model = User
        fields = ('otp',)

    def validate(self, attrs):
        email = self.context['request'].session.get('email')
        otp_model = Otp.objects.get(email=email)
        first_name = otp_model.first_name
        last_name = otp_model.last_name
        password = otp_model.password
        count = otp_model.count
        otp = otp_model.otp
        in_time = datetime.combine(datetime.today(),otp_model.in_time)
        time_now = datetime.now()
        delta= time_now - in_time
        if delta.total_seconds()/60 > 10:
            raise serializers.ValidationError('Otp has been Expired')

        if count >= 3:
            raise serializer.ValidationError('Otp attempts is Over')

        if otp != attrs['otp']:
            otp_model.count = count + 1
            otp_model.save()
            raise serializers.ValidationError(f'Wrong Otp. Only {3 - (count + 1)} attempts remaining.')

        if otp == attrs['otp'] and count <= 3:
            user = User(username=email, first_name=first_name, last_name=last_name, email=email, password=password)
            user.save()

        return attrs


        

#******************************* Login Serializer ****************************#

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    
    class Meta:
        model = User
        fields = ('email','password')
        extra_kwargs = {'password' : {'write_only' : True}}

    def validate(self, attrs):
        request = self.context['request']
        username = attrs['email']
        password = attrs['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            raise serializers.ValidationError('Invalid Username or Password')

        return attrs


    
#***************************** Change Password Serializer ***************************#

class ChangePasswordSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ('password', 'password2')
        extra_kwargs = {'password': {'write_only': True},'password2': {'write_only': True} }

    def validate(self, attrs):
        user = self.context.get('request').user
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password and password2 and password != password2:
            raise serializers.ValidationError("Password and Confirm Password Doesn't match.")
        user.set_password(password)
        user.save()
        return attrs


#******************************* Forget Password Serializer ********************************#
class ForgetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ('email',)

#******************** Validate Otp For Forget Password Serializer ***************************#

class ValidateOtpForForgetPasswordSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(max_length = 6)
    password2 = serializers.CharField(style={'input_type':'password'})

    class Meta:
        model = User
        fields = ('otp','password', 'password2')
        extra_kwargs = {'password': {'write_only': True},'password2': {'write_only': True} }

    def validate(self, attrs):
        email = self.context['request'].session.get('email')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        otp_model = Otp.objects.get(email=email)
        count = otp_model.count
        otp = otp_model.otp
        in_time = datetime.combine(datetime.today(),otp_model.in_time)
        time_now = datetime.now()
        delta= time_now - in_time

        if delta.total_seconds()/60 > 10:
            raise serializers.ValidationError('Otp has been Expired')

        if count >= 3:
            raise serializers.ValidationError('Otp attempts is Over')

        if otp != attrs['otp']:
            otp_model.count = count + 1
            otp_model.save()
            raise serializers.ValidationError(f'Wrong Otp. Only {3 - (count + 1)} attempts remaining.')

        if password and password2 and password == password2:
            if otp == attrs['otp'] and count <= 3:
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
        else:
            raise serializers.ValidationError('Password and Confirm Password is not matching')

        return attrs



class AttendenceSerializer(serializers.ModelSerializer):
    punch_status = serializers.BooleanField(allow_null=True)
    class Meta:
        model = Attendence
        fields = ('punch_status','date')        

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

