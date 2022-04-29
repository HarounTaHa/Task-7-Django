from django.contrib.auth import authenticate
from django.shortcuts import render

# Create your views here.

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view

from .models import MemberUser
from .serializers import LoginSerializer, RegisterSerializer
from rest_framework.response import Response


@api_view(['POST', 'OPTIONS'])
def login_point(request):
    serializers = LoginSerializer(data=request.data)
    if serializers.is_valid():
        return Response(serializers.data)
    return Response(serializers.errors)


@api_view(['POST', 'OPTIONS'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = MemberUser.objects.create_user(user_name=request.data['user_name'], email=request.data['email'],
                                              password=request.data['password'])
        token = Token.objects.get(user=user)
        return Response({'Register': True, 'token': str(token)})

    return Response(serializer.errors)
