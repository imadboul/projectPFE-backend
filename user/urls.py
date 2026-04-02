
from django.contrib import admin
from django.urls import path , include
from .views import signup ,login ,verifyEmail
urlpatterns = [
    path('signUp/', signup ),
    path('verifyEmail/<str:token>/', verifyEmail),
    path('login/', login),
]
