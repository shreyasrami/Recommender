import email
from os import stat
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, RecommendSerializer, UserDetailsSerializer, EditDetailsSerializer
from django.contrib import auth
from .models import User,PastRecommendations
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from .externals import getAllHospitals, rankFilter, getDocsByIds

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



# usr = User.objects.get(email=request.user)
# recom = list(temp['Sr No.'])
# recom_ids = list(map(int, recom))
# print(recom_ids)
# PastRecommendations.objects.create(patient=usr,past_recom=recom_ids)

class GetAllHospitalsView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        response = getAllHospitals()
        return Response(response,status=HTTP_200_OK)

class RecommendView(generics.GenericAPIView):
    serializer_class = RecommendSerializer
    permission_classes = (IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        serializer = RecommendSerializer(data=request.data)
        if serializer.is_valid():
            """ experience = serializer.validated_data['experience']
            fee = serializer.validated_data['fee']
            city_name = serializer.validated_data['city_name']
            temp = rankFilter(dataset, model, experience, fee, city_name, 10)
            recom_list = temp.iloc[:,0:13].drop(['unrequired'],axis=1).to_dict('records') """
            return Response(status=HTTP_200_OK)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)

class UserDetailsView(generics.GenericAPIView):
    serializer_class = UserDetailsSerializer
    permission_classes = ()

    def get(self,request,*args,**kwargs):
        if User.objects.filter(id=kwargs['user_id']):
            usr = User.objects.get(id=kwargs['user_id'])
            data = {
                'user_id': usr.id,
                'email': usr.email,
                'first_name': usr.fname,
                'last_name': usr.lname,
                'phone': usr.phone,
                'city': usr.city
            }
            return Response(data,status=HTTP_200_OK)
        else:
            return Response(status=HTTP_404_NOT_FOUND)
    


class EditDetailsView(generics.GenericAPIView):
    serializer_class = EditDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args,**kwargs):
        usr = User.objects.get(email=request.user)

        data = {
            'user_id': usr.id,
            'email': usr.email,
            'first_name': usr.fname,
            'last_name': usr.lname,
            'phone': usr.phone,
            'city': usr.city
        }
        return Response(data,status=HTTP_200_OK)
            

    def post(self,request,*args,**kwargs):
        usr = User.objects.get(email=request.user)
        serializer = EditDetailsSerializer(instance=usr,data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            data = {
                'updated': True,
                'user_id': user.id,
                'email': user.email,
                'first_name': user.fname,
                'last_name': user.lname,
                'phone': user.phone,
                'city': user.city
            }
        else:
            data = {
                'updated': False,
                'user_id': usr.id,
            }
        return Response(data,status=HTTP_200_OK)