from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_400_BAD_REQUEST
from .serializers import MainCommentSerializer, PostSerializer, SubCommentSerializer
from .models import PostModel,MainCommentModel,SubCommentModel
from django.contrib.auth.models import User
# Create your views here.


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def createPost(request):
    waste,token = request.headers['Authorization'].split(' ')
    user = Token.objects.get(key=token).user
    serializer = PostSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({"error":"All fields are required"},status=status.HTTP_400_BAD_REQUEST)
    post = PostModel.objects.create(
        title=serializer.data['title'],
        description=serializer.data['description'],
        author=user
        )
    if post is not None:
        post.save()
        return Response({"message":"Post has been created","details":{
            "title":post.title,
            "image":post.image,
            "description":post.description,
            "likes":post.likes,
            "author":user.username,
            "id":post.id
        }},status=status.HTTP_201_CREATED)
    return Response({"error":"All fields are required!"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def createMainComment(request):
    waste,token = request.headers['Authorization'].split(' ')
    user = Token.objects.get(key=token).user
    serializer = MainCommentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({"error":"All fields are required"},status=status.HTTP_400_BAD_REQUEST)
    post = PostModel.objects.get(id=serializer.data['main_post'])
    if post is not None:
        comment = MainCommentModel.objects.create(
            comment=serializer.data['comment'],
            author=user,
            main_post=post
        )
        if comment is not None:
            comment.save()
            return Response({"message":"Post has been created","details":{
                "comment":comment.comment,
                "author":user.username,
                "post":post.id,
                "id":comment.id
            }},status=status.HTTP_201_CREATED)  
        return Response({"error":"All fields are required!"},status=HTTP_400_BAD_REQUEST)
    return Response({"error":"The post no longer exists"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def createSubComment(request):
    waste,token = request.headers['Authorization'].split(' ')
    user = Token.objects.get(key=token).user
    serializer = SubCommentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({"error":"Comment dosent exists"},status=status.HTTP_400_BAD_REQUEST)
    main_comment = MainCommentModel.objects.get(id=serializer.data['main_comment'])
    if main_comment is not None:
        comment = SubCommentModel.objects.create(
            comment=serializer.data['comment'],
            author=user,
            main_comment=main_comment
        )
        if comment is not None:
            comment.save()
            return Response({"message":"Post has been created","details":{
                "comment":comment.comment,
                "author":user.username,
                "main_comment":main_comment.id,
                "id":comment.id
            }},status=status.HTTP_201_CREATED)  
        return Response({"error":"All fields are required!"},status=HTTP_400_BAD_REQUEST)
    return Response({"error":"The post no longer exists"},status=status.HTTP_400_BAD_REQUEST)