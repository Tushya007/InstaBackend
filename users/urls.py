from django.urls import path
from .views import signup,login,getUserByToken

urlpatterns = [
    path('signup/',signup),
    path('login/',login),
    path('get/username/',getUserByToken),
]