from django.shortcuts import render

from api.models import Event


def list_errors(request):
    events = Event.objects.all()

    context = {
        'events': events,
        'events_empty': []
    }

    return render(request, 'events/list.html', context=context)
