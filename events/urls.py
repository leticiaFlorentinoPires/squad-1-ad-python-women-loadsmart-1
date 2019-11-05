from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import NestedRouterMixin
from events import views
from events.views import EventsListView, EventFilter, EventDetail

router = routers.DefaultRouter()
router.register(r'events', views.EventAPIViewSet)
router.register(r'agents', views.AgentAPIViewSet)
router.register(r'users', views.UserAPIViewSet)
router.register(r'groups', views.GroupAPIViewSet)

#resource to get acess to get, post ,put , delete of /agent/id/event
class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass

#router for get acess to "get", "post", "put", "delete" of endpoint /agent/id/event
router_agent_events = NestedDefaultRouter()
agents_router = router_agent_events.register(r'agent', views.AgentAPIViewSet)
agents_router.register('events', views.EventAPIViewSet, basename='events-agents',
                       parents_query_lookups = ['agent'])

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(agents_router.router.urls)),
    path('', EventFilter.as_view(), name='events-list'),
    # re_path(r'agents/(?P<id_agent>\d+)/events/(?P<id_event>\d+)', agent_id_event_id , name='events_by_agents'),
    # path('<str:envName>', EventFilter.as_view(), name='filter_events'),
    path('<int:event_id>', EventDetail.as_view(), name='detail')
]