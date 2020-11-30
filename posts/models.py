from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PostModel(models.Model):
    title = models.CharField(max_length=200)
    image = models.CharField(max_length=3000,default="n/a")
    description = models.CharField(max_length=1000)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    date_time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class MainCommentModel(models.Model):
    comment = models.CharField(max_length=300)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    main_post = models.ForeignKey(PostModel,on_delete=models.CASCADE,null=True)
    date_time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


class SubCommentModel(models.Model):
    comment = models.CharField(max_length=300)
    main_comment = models.ForeignKey(MainCommentModel,on_delete=models.CASCADE,null=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    date_time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

class LikeModel(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel,on_delete=models.CASCADE)
    date_time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username