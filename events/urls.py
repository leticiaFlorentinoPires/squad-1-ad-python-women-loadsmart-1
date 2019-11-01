from django.urls import include, path, re_path
from rest_framework import routers
from events import views
from events.views import EventsListView, EventFilter, EventDetail

router = routers.DefaultRouter()
router.register(r'events', views.EventAPIViewSet)
router.register(r'agents', views.AgentAPIViewSet)
router.register(r'users', views.AgentAPIViewSet)
router.register(r'groups', views.AgentAPIViewSet)
agent_id_event_id = views.EventOfIdViewSet.as_view(
    {'get': 'event_id_agent_id'}
)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', EventFilter.as_view(), name='events-list'),
    re_path(r'agents/(?P<id_agent>\d+)/events/(?P<id_event>\d+)', agent_id_event_id , name='events_by_agents'),
    # path('<str:envName>', EventFilter.as_view(), name='filter_events'),
    path('<int:event_id>', EventDetail.as_view(), name='detail')
]