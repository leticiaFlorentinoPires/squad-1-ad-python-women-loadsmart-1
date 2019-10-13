from django.contrib import admin
from .models import User, Event, Log

admin.site.register(User)
admin.site.register(Event)
admin.site.register(Log)
