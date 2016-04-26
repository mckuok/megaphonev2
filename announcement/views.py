from django.shortcuts import render
from django.views.generic.edit import View
from django.http import JsonResponse, HttpResponse
from django.core import serializers

from .models import Announcement
from domains.models import Domain
from pages.models import Page

import json


# Create your views here.
class CreateAnnouncementView(View):

    def post(self, request, *args, **kwargs):
        dct = json.loads(request.body)
        role = dct['role']
        if role == 'domain':
            admin = Domain.objects.get(admin=request.user)
        else:
            admin = Page.objects.get(admin=request.user)
        new_announcement = Announcement(content_object=admin, text=dct['text'], level=dct['role'], title=dct['title'])
        new_announcement.save()
        return HttpResponse('')


class GetAnnouncementView(View):

    def get(self, request, *args, **kwargs):
        count = request.GET.get('count', 5)
        option = request.GET.get('range', 'all')
        target = request.GET.get('target', 'any')

        if option == all:
            announcements = Announcement.objects.all().order_by('-date_created')
        elif option == 'domain':
            if target == 'any':
                announcements = Announcement.objects.filter(level='domain').order_by('-date_created')
            else:
                admin = Domain.objects.get(admin=request.user)
                announcements = admin.announcements.all().order_by('-date_created')
        elif option == 'page':
            if target == 'any':
                announcements = Announcement.objects.filter(level='page').order_by('-date_created')
            else:
                admin = Page.objects.get(admin=request.user)
                announcements = admin.announcements.all().order_by('-date_created')

        if count != -1:
            announcements = announcements[: count]

        return JsonResponse(serializers.serialize('json', announcements), safe=False)
