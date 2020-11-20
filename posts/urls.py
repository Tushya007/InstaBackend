from django.urls import path
from .views import createPost,createMainComment,createSubComment

urlpatterns = [
    path('create/',createPost),
    path('create/maincomment/',createMainComment),
    path('create/subcomment/',createSubComment),
]