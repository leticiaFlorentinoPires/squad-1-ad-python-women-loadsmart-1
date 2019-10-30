from django.urls import include, path, re_path
from rest_framework import routers, urls
from events import views
from events.views import EventsListView, EventFilter, EventDetail

router = routers.DefaultRouter()
router.register(r'events', views.EventAPIViewSet)
router.register(r'agents', views.AgentAPIViewSet)
# router.register(r'agents/(<pk>\d+)/events',  views.EventsOfAgentViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('', EventFilter.as_view(), name='events-list'),
    # path('<str:envName>', EventFilter.as_view(), name='filter_events'),
    path('<int:event_id>', EventDetail.as_view(), name='detail')
]