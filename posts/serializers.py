from django.db.models import fields
from rest_framework import serializers
from .models import PostModel, MainCommentModel,SubCommentModel,LikeModel

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ('title','description')

class MainCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCommentModel
        fields = ('comment','main_post')

class SubCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCommentModel
        fields = ('comment','main_comment')

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeModel
        fields = ['post']