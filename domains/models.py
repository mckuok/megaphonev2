from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from announcement.models import Announcement
from event.models import Event


# Create your models here.
class Domain(models.Model):
    admin = models.ForeignKey('users.User')
    name = models.CharField(max_length=40)
    domainID = models.CharField(max_length=20, unique=True, default='')
    description = models.TextField(max_length=200, default='')
    memberNum = models.IntegerField(default=0)
    announcements = GenericRelation(Announcement)
    events = GenericRelation(Event)

    def __unicode__(self):
        return self.name

    def get_content_type(self):
        return ContentType.objects.get_for_model(self).id