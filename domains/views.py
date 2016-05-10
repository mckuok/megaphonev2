from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.views.generic.edit import View

from .models import Domain
from announcement.models import Announcement
from event.models import Event, EventGoer
from pages.models import Page
from users.views import update_last_login_field

import json
from datetime import datetime, timedelta
from itertools import chain


# Create your views here.
class GetDomainsView(View):

    def get(self, request, *args, **kwargs):
        domains = Domain.objects.all()
        return JsonResponse(serializers.serialize('json', domains), safe=False)


class SubscribeDomainView(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        subscribedDomain = filter(bool, user.subscribe_domain.split(' '))
        domains = []
        for i in range(len(subscribedDomain)):
            domain = Domain.objects.get(pk=subscribedDomain[i])
            domains.append(domain)
        # return HttpResponse(json.dumps(domains), content_type='application/json')
        return JsonResponse(serializers.serialize('json', domains), safe=False)

    def post(self, request, *args, **kwargs):
        pk = kwargs['domain_pk'].encode('utf-8')
        user = request.user
        user.subscribe_domain = user.subscribe_domain + " " + pk
        user.subscribe_domain = user.subscribe_domain.strip()
        user.save()
        domain = Domain.objects.get(id=pk)
        domain.memberNum += 1
        domain.save()
        return HttpResponse(serializers.serialize("json", [domain]))


class DomainHomeView(View):

    def get(self, request, *args, **kwargs):
        admin = Domain.objects.get(admin=request.user)
        current_list = admin.announcements.all()
        if current_list.count() > 0:
            current_announcement = current_list.order_by('-date_created')[0]
        else:
            current_announcement = None

        history_list = Announcement.objects.filter(level='page', date_created__gte=datetime.now() - timedelta(days=7))
        matched_list = []

        fitted = 0
        for announcement in history_list:
            if announcement.content_object.domain == admin:
                matched_list.append(announcement)
                fitted += 1
                if fitted == 5:
                    break

        if len(matched_list) > 0:
            matched_list.sort(key=lambda x: x.date_created, reverse=True)

        is_pageAdmin = False
        if Page.objects.filter(admin=request.user).count() > 0:
            is_pageAdmin = True

        return render(request, 'domain_home_announcement.html', {'current_announcement': current_announcement,
                                                                 'history_announcements': matched_list,
                                                                 'name': admin.name,
                                                                 'is_member': True,
                                                                 'is_pageAdmin': is_pageAdmin,
                                                                 'is_domainAdmin': True})


class DomainHomeEventView(View):

    def get(self, request, *args, **kwargs):
        admin = Domain.objects.get(admin=request.user)
        current_list = admin.events.all()
        current_list = current_list.filter(date_event__gte=datetime.now())
        user_event_list = []
        if current_list.count() > 0:
            current_list = current_list.order_by('date_event')
            for event in current_list:
                event_goers = EventGoer.objects.filter(event=event)
                goer_list = []
                for goer in event_goers:
                    goer_list.append([goer.user.name, goer.user.email])
                user_event_list.append([event, goer_list])

        history_list = Event.objects.filter(level='page', date_end__gte=datetime.now())
        history_list = history_list.order_by('date_event')
        matched_list = []
        fitted = 0
        for event in history_list:
            if event.content_object.domain == admin:
                matched_list.append(event)
                fitted += 1
                if fitted == 5:
                    break

        pages = Page.objects.filter(domain=admin)
        pages_events = []
        pages_events.append(admin.events.all())
        for page in pages:
            pages_events.append(page.events.all())

        all_events = []
        for event_list in pages_events:
            for event in event_list:
                all_events.append(event)

        is_pageAdmin = False
        if Page.objects.filter(admin=request.user).count() > 0:
            is_pageAdmin = True

        update_last_login_field(request.user)
        return render(request, 'domain_home_event.html', {'ongoing_events': user_event_list,
                                                          'history_events': matched_list,
                                                          'all_events': all_events,
                                                          'name': admin.name,
                                                          'is_member': True,
                                                          'is_pageAdmin': is_pageAdmin,
                                                          'is_domainAdmin': True})


class DomainProfileView(View):

    def get(self, request, *args, **kwargs):
        pk = kwargs['domain_pk'].encode('utf-8')
        current_list = Domain.objects.get(pk=pk).announcements.all()
        if current_list.count() > 0:
            current_announcement = current_list.order_by('-date_created')[0]
        else:
            current_announcement = None

        current_list = Domain.objects.get(pk=pk).events.all()
        current_list = current_list.filter(date_event__gte=datetime.now())
        if current_list.count() > 0:
            current_list = current_list.order_by('date_event')

        return render(request, 'profile.html', {'current_announcement': current_announcement,
                                                'current_events': current_list})
