from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from .serializers import MainCommentSerializer, PostSerializer, SubCommentSerializer, LikeSerializer
from .models import PostModel, MainCommentModel, SubCommentModel, LikeModel
from django.contrib.auth.models import User
# Create your views here.


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def createPost(request):
    waste, token = request.headers['Authorization'].split(' ')
    user = Token.objects.get(key=token).user
    serializer = PostSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)
    post = PostModel.objects.create(
        title=serializer.data['title'],
        description=serializer.data['description'],
        author=user
    )
    if post is not None:
        content = {"message": "Post has been created", "details": {
            "title": post.title,
            "image": post.image,
            "description": post.description,
            "author": user.username,
            "id": post.id
        }}
        post.save()
        return Response(content, status=status.HTTP_201_CREATED)
    return Response({"error": "All fields are required!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def createMainComment(request):
    waste, token = request.headers['Authorization'].split(' ')
    user = Token.objects.get(key=token).user
    serializer = MainCommentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)
    post = PostModel.objects.get(id=serializer.data['main_post'])
    if post is not None:
        comment = MainCommentModel.objects.create(
            comment=serializer.data['comment'],
            author=user,
            main_post=post
        )
        if comment is not None:
            content = {"message": "Post has been created", "details": {
                "comment": comment.comment,
                "author": user.username,
                "post": post.id,
                "id": comment.id
            }}
            comment.save()
            return Response(content, status=status.HTTP_201_CREATED)
        return Response({"error": "All fields are required!"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "The post no longer exists"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def createSubComment(request):
    waste, token = request.headers['Authorization'].split(' ')
    user = Token.objects.get(key=token).user
    serializer = SubCommentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({"error": "Comment dosent exists"}, status=status.HTTP_400_BAD_REQUEST)
    main_comment = MainCommentModel.objects.get(
        id=serializer.data['main_comment'])
    if main_comment is not None:
        comment = SubCommentModel.objects.create(
            comment=serializer.data['comment'],
            author=user,
            main_comment=main_comment
        )
        if comment is not None:
            content = {"message": "Post has been created", "details": {
                "comment": comment.comment,
                "author": user.username,
                "main_comment": main_comment.id,
                "id": comment.id
            }}
            comment.save()
            return Response(content, status=status.HTTP_201_CREATED)
        return Response({"error": "All fields are required!"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "The post no longer exists"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def likePost(request):
    waste, token = request.headers['Authorization'].split(' ')
    user = Token.objects.get(key=token).user
    serializer = LikeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({"error": "Post dosent exists"}, status=status.HTTP_400_BAD_REQUEST)
    post = PostModel.objects.get(id=serializer.data['post'])
    if post is None:
        return Response({"error": "Post dosent exists"}, status=status.HTTP_400_BAD_REQUEST)
    like = LikeModel.objects.create(post=post, author=user)
    if like is not None:
        content = {
            "message": "Like added"
        }
        like.save()
        return JsonResponse(content, status=status.HTTP_201_CREATED)
    return Response({"error": "The post no longer exists"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def getAllPosts(request):
    qs_post = PostModel.objects.all()
    final_content = []
    for post in qs_post:
        sub_content = {
            "title": post.title,
            "image": post.image,
            "description": post.description,
            "likes": [],
            "author": post.author.username,
            "id": post.id,
            "comments": []
        }
        qs_likes = LikeModel.objects.filter(post=post)
        for like in qs_likes:
            main_like_content = {
                "post": like.post.id,
                "author": like.author.username,
            }
            sub_content['likes'].append(main_like_content)
        qs_mainComments = MainCommentModel.objects.filter(main_post_id=post.id)
        for mainComment in qs_mainComments:
            main_comment_content = {
                "comment": mainComment.comment,
                "author": mainComment.author.username,
                "post": post.id,
                "id": mainComment.id,
                "sub_comments": []
            }
            qs_subComments = SubCommentModel.objects.filter(
                main_comment_id=mainComment.id)
            for subComment in qs_subComments:
                sub_comment_content = {
                    "comment": subComment.comment,
                    "author": subComment.author.username,
                    "main_comment": mainComment.id,
                    "id": subComment.id
                }
                main_comment_content['sub_comments'].append(
                    sub_comment_content)
            sub_content['comments'].append(main_comment_content)
        final_content.append(sub_content)
    return Response(final_content, status=status.HTTP_200_OK)
