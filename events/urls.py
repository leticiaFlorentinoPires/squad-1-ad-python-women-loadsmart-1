from django.conf.urls import url
from django.urls import include, path, re_path
from rest_framework import routers, urls
from events import views
from events.views import EventsListView, EventFilter, EventDetail

router = routers.DefaultRouter()
router.register(r'events', views.EventAPIViewSet)
router.register(r'agents', views.AgentAPIViewSet)


events_agent_id = views.EventsOfAgentViewSet.as_view(
    {'get': 'list_events_of_agent',
     'post': 'include_event_in_agent',
     'put': 'partial_update',
     'delete': 'destroy'
     }
)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', EventFilter.as_view(), name='events-list'),
    re_path(r'agents/(?P<id>\d+)/events/', events_agent_id, name= 'events_by_agents'),
    # path('<str:envName>', EventFilter.as_view(), name='filter_events'),
    path('<int:event_id>', EventDetail.as_view(), name='detail')
]

