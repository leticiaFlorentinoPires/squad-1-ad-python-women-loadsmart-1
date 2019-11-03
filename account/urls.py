# account/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    #path('password_reset/', views.forgotPassword, name='password_reset'),
]