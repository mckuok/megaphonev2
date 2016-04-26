from django.shortcuts import render, redirect
from django.views.generic.edit import FormView, CreateView, View
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone

from .forms import MemberRegistrationForm, AuthForm
from .models import User

from domains.forms import DomainRegistrationForm
from domains.models import Domain

from pages.forms import PageRegistrationForm
from pages.models import Page

from event.models import Event

from datetime import datetime, timedelta


def update_last_login_field(user):
    if user.is_authenticated():
        user.last_access = timezone.now()
        user.save()


class HomeView(FormView):

    def get(self, request, *args, **kwargs):
        logout(request)
        if request.user.is_authenticated():
            return redirect('/%s' % request.user.role)
        else:
            return render(request, 'home.html', {'form': AuthForm})

    def post(self, request, *args, **kwargs):
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/%s' % user.role)
        else:
            return render(request, 'home.html', {'form': form})


class MemberRegistrationView(CreateView):
    template_name = 'member_registration.html'
    form_class = MemberRegistrationForm
    model = User

    def form_valid(self, form):
        user = User.objects.create(email=form.cleaned_data['email'], name=form.cleaned_data['name'])
        user.set_password(form.cleaned_data['password2'])
        user.role = 'member'
        user.save()
        authenticated_user = authenticate(username=user.email, password=form.cleaned_data['password2'])
        login(self.request, authenticated_user)
        return redirect('/member')


class MemberHomeEventView(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        domain_list = user.subscribe_domain.strip()
        page_list = user.subscribe_page.strip()

        if domain_list == "":
            display_search_box = True
        else:
            display_search_box = False

        subscribed_domain = filter(bool, domain_list.split(' '))
        subscribed_page = filter(bool, page_list.split(' '))
        domains = {}
        domains_announcement = {}
        announcement_limit = 7
        new_announcement_count = 0
        last_login_date = user.last_access
        for i in range(len(subscribed_domain)):
            domain = Domain.objects.get(pk=subscribed_domain[i])
            domains[domain.name] = []

            current_list = domain.announcements.all().filter(
                date_created__gte=datetime.now()-timedelta(days=announcement_limit))

            if current_list.count() > 0:
                new_announcement_count = new_announcement_count + current_list.filter(date_created__gte=last_login_date).count()
                current_announcement = current_list.order_by('-date_created')[0]
            else:
                current_announcement = None

            domains_announcement[domain.name] = current_announcement

        pages_announcement = {}
        for i in range(len(subscribed_page)):
            page = Page.objects.get(pk=subscribed_page[i])
            domains[page.domain.name].append(page.name)

            current_list = page.announcements.all().filter(
                date_created__gte=datetime.now()-timedelta(days=announcement_limit))

            if current_list.count() > 0:
                new_announcement_count = new_announcement_count + current_list.filter(date_created__gte=last_login_date).count()
                current_announcement = current_list.order_by('-date_created')[0]
            else:
                current_announcement = None

            pages_announcement[page.name] = current_announcement

        all_event = Event.objects.all()
        new_events = all_event.filter(date_created__gte=last_login_date)
        new_events_count = new_events.count()

        update_last_login_field(user)
        return render(request, 'member_home.html', {'displaySearchBox': display_search_box,
                                                    'new_announcement_count': new_announcement_count,
                                                    'event_list': all_event,
                                                    'new_event': new_events,
                                                    'new_events_count': new_events_count,
                                                    'domain_list': domains,
                                                    'today': datetime.now()})


class MemberHomeAnnouncementView(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        domain_list = user.subscribe_domain.strip()
        page_list = user.subscribe_page.strip()

        subscribed_domain = filter(bool, domain_list.split(' '))
        subscribed_page = filter(bool, page_list.split(' '))
        domains = {}
        domains_announcement = {}
        announcement_limit = 7
        new_announcement_count = 0
        last_login_date = user.last_access
        for i in range(len(subscribed_domain)):
            domain = Domain.objects.get(pk=subscribed_domain[i])
            domains[domain.name] = []

            current_list = domain.announcements.all().filter(
                date_created__gte=datetime.now()-timedelta(days=announcement_limit))

            if current_list.count() > 0:
                new_announcement_count = new_announcement_count + current_list.filter(date_created__gte=last_login_date).count()
                current_announcement = current_list.order_by('-date_created')[0]
            else:
                current_announcement = None

            domains_announcement[domain.name] = current_announcement

        pages_announcement = {}
        for i in range(len(subscribed_page)):
            page = Page.objects.get(pk=subscribed_page[i])
            domains[page.domain.name].append(page.name)

            current_list = page.announcements.all().filter(
                date_created__gte=datetime.now()-timedelta(days=announcement_limit))

            if current_list.count() > 0:
                new_announcement_count = new_announcement_count + current_list.filter(date_created__gte=last_login_date).count()
                current_announcement = current_list.order_by('-date_created')[0]
            else:
                current_announcement = None

            pages_announcement[page.name] = current_announcement

        update_last_login_field(user)
        return render(request, 'member_home_announcement.html', {'domains_announcement': domains_announcement,
                                                    'pages_announcement': pages_announcement,
                                                    'new_announcement_count': new_announcement_count,
                                                    'domain_list': domains,
                                                    'today': datetime.now()})


class DomainRegistrationView(FormView):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            authenticated = True
        else:
            authenticated = False

        return render(request, 'domain_registration.html', {'auth_form': AuthForm,
                                                            'member_form': MemberRegistrationForm,
                                                            'domain_form': DomainRegistrationForm,
                                                            'auth_form_submitted': False,
                                                            'member_form_submitted': False,
                                                            'authenticated': authenticated,
                                                            'warnings': ''})

    def post(self, request, *args, **kwargs):
        auth_form = AuthForm(data=request.POST)
        member_form = MemberRegistrationForm(data=request.POST)
        domain_form = DomainRegistrationForm(data=request.POST)
        warnings = ''

        if request.user.is_authenticated():
            if Domain.objects.filter(admin=request.user).count() > 0:
                warnings = "<strong> Error: </strong> You can only register one domain per account"
            authenticated = True
        else:
            authenticated = False

        if auth_form.has_changed():
            auth_form_submitted = True
        else:
            auth_form_submitted = False

        if member_form.has_changed():
            member_form_submitted = True
        else:
            member_form_submitted = False

        if auth_form.has_changed() and auth_form.is_valid():
            user = auth_form.get_user()
            if Domain.objects.filter(admin=user).count() == 0:
                user.role = 'domainAdmin'
                user.save()
                login(request, user)
                authenticated = True
            else:
                warnings = "<strong> Error: </strong> You can only register one domain per account"

        elif member_form.has_changed() and member_form.is_valid():
            user = User.objects.create(email=member_form.cleaned_data['email'], name=member_form.cleaned_data['name'])
            user.set_password(member_form.cleaned_data['password2'])
            user.role = 'domainAdmin'
            user.save()
            authenticated_user = authenticate(username=user.email, password=member_form.cleaned_data['password2'])
            login(self.request, authenticated_user)
            authenticated = True

        if authenticated is True and domain_form.is_valid() and len(warnings) == 0:
            user = request.user
            domain = Domain.objects.create(admin=user, name=domain_form.cleaned_data['name'],
                                           domainID=domain_form.cleaned_data['domainID'],
                                           description=domain_form.cleaned_data['description'])
            domain.save()
            return redirect('/domainAdmin')

        return render(request, 'domain_registration.html', {'auth_form': auth_form,
                                                            'member_form': member_form,
                                                            'domain_form': domain_form,
                                                            'warnings': warnings,
                                                            'auth_form_submitted': auth_form_submitted,
                                                            'member_form_submitted': member_form_submitted,
                                                            'authenticated': authenticated})


class PageRegistrationView(FormView):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            authenticated = True
        else:
            authenticated = False

        return render(request, 'page_registration.html', {'auth_form': AuthForm,
                                                          'member_form': MemberRegistrationForm,
                                                          'page_form': PageRegistrationForm,
                                                          'auth_form_submitted': False,
                                                          'member_form_submitted': False,
                                                          'authenticated': authenticated,
                                                          "warnings": ''})

    def post(self, request, *args, **kwargs):
        auth_form = AuthForm(data=request.POST)
        member_form = MemberRegistrationForm(data=request.POST)
        page_form = PageRegistrationForm(data=request.POST)
        warnings = ''

        if request.user.is_authenticated():
            if Domain.objects.filter(admin=request.user).count() > 0:
                warnings = "<strong> Error: </strong> You can only register one domain per account"
            authenticated = True
        else:
            authenticated = False

        if auth_form.has_changed() :
            auth_form_submitted = True
        else:
            auth_form_submitted = False

        if member_form.has_changed() :
            member_form_submitted = True
        else:
            member_form_submitted = False

        if auth_form.has_changed() and auth_form.is_valid():
            user = auth_form.get_user()
            if Domain.objects.filter(admin=user).count() == 0:
                user.role = 'pageAdmin'
                user.save()
                login(request, user)
                authenticated = True
            else:
                warnings = "<strong> Error: </strong> You can only register one domain per account"

        elif member_form.has_changed() and member_form.is_valid():
            user = User.objects.create(email=member_form.cleaned_data['email'], name=member_form.cleaned_data['name'])
            user.set_password(member_form.cleaned_data['password2'])
            user.role = 'pageAdmin'
            user.save()
            authenticated_user = authenticate(username=user.email, password=member_form.cleaned_data['password2'])
            login(self.request, authenticated_user)
            authenticated = True

        if authenticated is True and page_form.is_valid():
            user = request.user
            page = Page.objects.create(domain=page_form.cleaned_data['referenceID'],
                                       admin=user, name=page_form.cleaned_data['name'],
                                       pageID=page_form.cleaned_data['pageID'],
                                       description=page_form.cleaned_data['description'])
            page.save()
            return redirect('/pageAdmin')

        return render(request, 'page_registration.html', {'auth_form': auth_form,
                                                          'member_form': member_form,
                                                          'page_form': page_form,
                                                          'auth_form_submitted': auth_form_submitted,
                                                          'member_form_submitted': member_form_submitted,
                                                          'authenticated': authenticated,
                                                          'warnings': warnings})


def log_out_view(request):
    logout(request)
    return redirect('/')

