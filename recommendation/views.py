from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib import auth
from .models import User
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK

# Create your views here.


class RegisterUserView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self,request,*args,**kwargs):
        
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            data = {
                'token': str(refresh.access_token),
                'user_id':user.id
            }
            return Response(data,status=HTTP_200_OK)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)
        
class LoginUserView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request,*args,**kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = auth.authenticate(email=email,password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                data = {
                    'token': str(refresh.access_token),
                    'user_id':user.id
                }
                return Response(data,status=HTTP_200_OK)
            else:                                                                                                    
                return Response({"status":"401_AUTHENTICATION_ERROR"})

        else:
            return Response(status=HTTP_400_BAD_REQUEST)
