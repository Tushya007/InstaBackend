from django.urls import path
from .views import createPost,createMainComment,createSubComment,getAllPosts,likePost

urlpatterns = [
    path('create/',createPost),
    path('create/maincomment/',createMainComment),
    path('create/subcomment/',createSubComment),
    path('get/all/',getAllPosts),
    path('like/',likePost),
]