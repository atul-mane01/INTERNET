from django.contrib import admin
from django.urls import path,include
from .views import UserRegistrationView,UserLoginView,UserProfileView,UserPasswordChange,SendPasswordEmail,UserPasswordResetView
urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('profile/',UserProfileView.as_view()),
    path('changepassword/',UserPasswordChange.as_view()),
    path('reset-password-email/',SendPasswordEmail.as_view()),
    path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view()),

]
