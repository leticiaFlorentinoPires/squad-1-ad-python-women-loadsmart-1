from django.urls import include, path, re_path
from rest_framework import routers
from events import views


router = routers.DefaultRouter()
router.register(r'events', views.EventAPIViewSet)
router.register(r'logs', views.AgentAPIViewSet)

urlpatterns = [
    path('', include(router.urls)),
    ]