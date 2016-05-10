from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.views.generic.edit import View

from domains.models import Domain
from pages.models import Page
from announcement.models import Announcement
from event.models import Event
from users.views import update_last_login_field

import json
from datetime import datetime, timedelta


# Create your views here.
class GetPagesView(View):

    def get(self, request, *args, **kwargs):
        pk = request.GET.get('pk', -1)
        user = request.user
        if pk == -1:
            subscribedDomain = filter(bool, user.subscribe_domain.split(' '))
            print(subscribedDomain)
            pages = {}
            for i in range(len(subscribedDomain)):
                domain = Domain.objects.get(pk=subscribedDomain[i])
                page = Page.objects.filter(domain=domain)
                if page:
                    pages[domain.name] = serializers.serialize('json', page)
                else:
                    pages[domain.name] = None
            print(json.dumps(pages))
            return HttpResponse(json.dumps(pages), content_type='application/json')
        else:
            page = Page.objects.get(id=pk)
            return HttpResponse(serializers.serialize("json", [page]))


class SubscribePageView(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        subscribedPage = filter(bool, user.subscribe_page.split(' '))
        pages = []
        for i in range(len(subscribedPage)):
            page = Page.objects.get(pk=subscribedPage[i])
            pages.append(page)
        return JsonResponse(serializers.serialize('json', pages), safe=False)

    def post(self, request, *args, **kwargs):
        pk = kwargs['page_pk'].encode('utf-8')
        user = request.user
        user.subscribe_page = user.subscribe_page + " " + pk
        user.subscribe_page = user.subscribe_page.strip()
        user.save()
        page = Page.objects.get(id=pk)
        page.memberNum += 1
        page.save()
        return HttpResponse(serializers.serialize("json", [page]))


class PageHomeView(View):

    def get(self, request, *args, **kwargs):
        page = Page.objects.get(admin=request.user)
        current_list = page.announcements.all()
        if current_list.count() > 0:
            current_announcement = current_list.order_by('-date_created')[0]
        else:
            current_announcement = None

        domain = page.domain
        domain_announcement = domain.announcements.all()
        if domain_announcement.count() > 0:
            domain_announcement = domain_announcement.order_by('-date_created')[0]
        else:
            domain_announcement = None

        is_domainAdmin = False
        if Domain.objects.filter(admin=request.user).count() > 0:
            is_domainAdmin = True

        update_last_login_field(request.user)
        return render(request, 'page_home.html', {'current_announcement': current_announcement,
                                                  'domain_announcement': domain_announcement,
                                                  'is_member': True,
                                                  'is_pageAdmin': True,
                                                  'is_domainAdmin': is_domainAdmin})


class PageHomeEventView(View):

    def get(self, request, *args, **kwargs):
        page = Page.objects.get(admin=request.user)
        page_list = page.events.all()
        current_list = page_list.filter(date_event__gte=datetime.now())
        if current_list.count() > 0:
            current_list = current_list.order_by('date_event')

        domain = page.domain
        domain_list = domain.events.all()
        if domain_list.count() > 0:
            domain_events = domain_list.filter(date_end__gte=datetime.now())
        else:
            domain_events = []

        all_events = []
        for event in page_list:
            all_events.append(event)
        for event in domain_list:
            all_events.append(event)

        is_domainAdmin = False
        if Domain.objects.filter(admin=request.user).count() > 0:
            is_domainAdmin = True

        update_last_login_field(request.user)
        return render(request, 'page_home_event.html', {'ongoing_events': current_list,
                                                        'domain_events': domain_events,
                                                        'all_events': all_events,
                                                        'is_member': True,
                                                        'is_pageAdmin': True,
                                                        'is_domainAdmin': is_domainAdmin})

class PageProfileView(View):

    def get(self, request, *args, **kwargs):
        pk = kwargs['page_pk'].encode('utf-8')
        current_list = Page.objects.get(pk=pk).announcements.all()
        if current_list.count() > 0:
            current_announcement = current_list.order_by('-date_created')[0]
        else:
            current_announcement = None

        current_list = Page.objects.get(pk=pk).events.all()
        current_list = current_list.filter(date_event__gte=datetime.now())
        if current_list.count() > 0:
            current_list = current_list.order_by('date_event')

        return render(request, 'profile.html', {'current_announcement': current_announcement,
                                                'current_events': current_list})
