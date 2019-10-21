from django.urls import include, path, re_path

from events import views

urlpatterns = [
    path('', views.list_events, name='list'),
    path('<int:event_id>', views.get_event, name='detail')
]