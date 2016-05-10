from django.shortcuts import render
from django.views.generic.edit import View
from django.http import JsonResponse, HttpResponse
from django.core import serializers

from .models import Event, EventGoer
from domains.models import Domain
from pages.models import Page

import json


# Create your views here.
class CreateEventView(View):

    def post(self, request, *args, **kwargs):
        dct = json.loads(request.body)
        print(dct)
        role = dct['role']
        if role == 'domain':
            admin = Domain.objects.get(admin=request.user)
        else:
            admin = Page.objects.get(admin=request.user)
        new_event = Event(content_object=admin, name=dct['name'], date_event=dct['date_event'],
                          date_end=dct['date_end'], location=dct['location'], function=dct['func'],
                          description=dct['description'], level=dct['role'])
        new_event.save()
        return HttpResponse('')


class GetEventView(View):

    def get(self, request, *args, **kwargs):
        count = request.GET.get('count', 5)
        option = request.GET.get('range', 'all')
        target = request.GET.get('target', 'any')

        if option == all:
            events = Event.objects.all().order_by('date_event')
        elif option == 'domain':
            if target == 'any':
                events = Event.objects.filter(level='domain').order_by('date_event')
            else:
                admin = Domain.objects.get(admin=request.user)
                events = admin.events.all().order_by('date_event')
        elif option == 'page':
            if target == 'any':
                events = Event.objects.filter(level='page').order_by('date_event')
            else:
                admin = Page.objects.get(admin=request.user)
                events = admin.events.all().order_by('date_event')

        if count != -1:
            events = events[: count]

        return JsonResponse(serializers.serialize('json', events), safe=False)


class GoingEventView(View):

    def post(self, request, *args, **kwargs):
        pk = kwargs['event_pk'].encode('utf-8')
        event = Event.objects.get(id=pk)
        event.goers += 1
        event.save()
        user = request.user
        EventGoer.objects.create(user=user, event=event)
        return HttpResponse('done')

