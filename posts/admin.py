from django.contrib import admin
from .models import PostModel,MainCommentModel,SubCommentModel

# Register your models here.
admin.site.register(PostModel)
admin.site.register(MainCommentModel)
admin.site.register(SubCommentModel)