from os import stat
from .serializers import UserSerializer,UserLoginSerializer
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
import bcrypt
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({"message":"User already exists"},status=status.HTTP_400_BAD_REQUEST)
    hashed_password = bcrypt.hashpw(serializer.data['password'].encode(),bcrypt.gensalt())
    user = User.objects.create(username=serializer.data['username'],email=serializer.data['email'],password=hashed_password)
    if user is not None:
        token = Token.objects.create(user=user)
        user.save()
        content = {
            "message":"User has been created",
            "details":{
                "username":user.username,
                "email":user.email,
                "token":token.key
            }
        }   
        return Response(content,status=status.HTTP_201_CREATED)
    return Response({"message":"server error"},status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serialzer = UserLoginSerializer(data=request.data)
    if serialzer.is_valid():
        return Response({"message":"Wrong credentials"},status=status.HTTP_401_UNAUTHORIZED)
    user_by_username = User.objects.filter(username=serialzer.data['username']).first()
    if user_by_username is not None:
        _password = serialzer.data['password'].encode()
        hspw = user_by_username.password.split("'")[1].encode()
        valid = bcrypt.checkpw(_password,hspw)
        if valid:
            token = Token.objects.get(user=user_by_username)
            return Response({"message":"User loggen in!","details":{"username":user_by_username.username,"token":token.key}})
    return Response({"message":"Wrong credentials"},status=status.HTTP_401_UNAUTHORIZED)