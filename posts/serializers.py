from rest_framework import serializers
from .models import PostModel, MainCommentModel,SubCommentModel

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