from .utils import Util
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode

from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework import serializers
from .models import User

class UserRegistrationSerializers(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model=User
        fields=['email','name','password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def validate(self,attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('password and conirm password does not match')
        return attrs


    def create(self,validate_data):
        return User.objects.create_user(**validate_data)


class UserLoginSerializers(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=50)
    class Meta:
        model=User
        fields=['email','password']

class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email']

class UserChangePasswordSerializers(serializers.ModelSerializer):
    # class User
    password=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        fields=['password','password2']
        model=User

    def validate(self,attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        user=self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('password and conirm password does not match')

        user.set_password(password)
        user.save()
        return attrs

class SendPasswordEmailSerializers(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=200)
    class Meta:
        fields=['email']
        model=User

    def validate(self,attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            print("uid=",uid)
            token=PasswordResetTokenGenerator().make_token(user)
            print(token)
            link="http://3000/api/user/reset/"+uid+'/'+token
            # send email
            body="Click Following link to reset password" 
            data={
                'subject':'Reset Your Password',
                'body':link,
                'to_email':user.email,
            }
            Util.send_email(data)



            print("password link",link)
            return attrs

        else:
            raise ValidationError('You are not register User')
        
class UserPasswordResetViewSerializers(serializers.ModelSerializer):
    password=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    
    class Meta:
        fields=['password','password2']
        model=User

    def validate(self,attrs):
        try:
            password=attrs.get('password')
            password2=attrs.get('password2')
            uid=self.context.get('uid')
            token=self.context.get('token')

            if password != password2:
                raise serializers.ValidationError('password and conirm password does not match')
            id=smart_str(urlsafe_base64_decode(uid))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationError('Token is not valid or expiresd')

            user.set_password(password)
            user.save()
            return attrs

        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationError('Token is not valid or expiresd')
        