from django.contrib import admin
from .models import PostModel,MainCommentModel,SubCommentModel,LikeModel

# Register your models here.
admin.site.register(PostModel)
admin.site.register(MainCommentModel)
admin.site.register(SubCommentModel)
admin.site.register(LikeModel)