from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Event, Log
from .serializers import (
    UserModelSerializer,
    EventModelSerializer,
    LogModelSerializer
)

class UserAPIViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

class EventAPIViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventModelSerializer

class LogAPIViewSet(viewsets.ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogModelSerializer