from django.urls import include, path, re_path
from rest_framework import routers

from events import views

router = routers.DefaultRouter()
router.register(r'events', views.EventAPIViewSet)
router.register(r'agents', views.AgentAPIViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.list_events, name='list_events'),
    path('<str:envName>/', views.post_detail, name='post_detail'),
    path('<int:event_id>', views.get_event, name='detail')
]