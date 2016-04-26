from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin

from users import views as userView
from domains import views as domainView
from pages import views as pageView
from event import views as eventView
from announcement import views as announceView


urlpatterns = [
    # Examples:
    # url(r'^$', 'megaphone.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', userView.HomeView.as_view(), name='home'),
    url(r'^register/member$', userView.MemberRegistrationView.as_view(), name='register member'),
    url(r'^register/domain$', userView.DomainRegistrationView.as_view(), name='register domain'),
    url(r'^register/page$', userView.PageRegistrationView.as_view(), name='register page'),
    url(r'^member/event$', userView.MemberHomeEventView.as_view(), name='member home'),
    url(r'^member/announcement$', userView.MemberHomeAnnouncementView.as_view(), name='member announcement home'),
    url(r'^domainAdmin$', domainView.DomainHomeView.as_view(), name='domain admin home'),
    url(r'^domainAdmin/event$', domainView.DomainHomeEventView.as_view(), name="domain admin home's event page"),
    url(r'^pageAdmin$', pageView.PageHomeView.as_view(), name='domain admin home'),
    url(r'^pageAdmin/event$', pageView.PageHomeEventView.as_view(), name="domain admin home's event page"),

    # url(r'^logout$', userView.LogOutView, name='logout'),
    url(r'^get/domain$', domainView.GetDomainsView.as_view(), name='list of domains'),
    url(r'^get/pages/$', pageView.GetPagesView.as_view(), name='list of pages'),
    url(r'^get/announcement/$', announceView.GetAnnouncementView.as_view(), name='get announcements'),
    url(r'^get/event/$', eventView.GetEventView.as_view(), name='get announcements'),
    url(r'^subscribe/domain/$', domainView.SubscribeDomainView.as_view(), name='get subscribed domains'),
    url(r'^subscribe/domain/(?P<domain_pk>\d+)/$', domainView.SubscribeDomainView.as_view(), name='subscribe to domain'),
    url(r'^subscribe/page/$', pageView.SubscribePageView.as_view(), name='get subscribed pages'),
    url(r'^subscribe/page/(?P<page_pk>\d+)/$', pageView.SubscribePageView.as_view(), name='subscribe to page'),
    url(r'^create/event/$', eventView.CreateEventView.as_view(), name='create an event'),
    url(r'^create/announcement/$', announceView.CreateAnnouncementView.as_view(), name='create an event'),
    url(r'^admin/', include(admin.site.urls)),
]
