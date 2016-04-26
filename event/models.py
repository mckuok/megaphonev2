from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=50, default=None)
    date_created = models.DateTimeField(auto_now=True)
    date_event = models.DateTimeField(null=True, blank=True, default=None)
    date_end = models.DateTimeField(null=True, blank=True, default=None)
    location = models.CharField(max_length=30, default=None)
    function = models.CharField(max_length=20, default=None)
    description = models.TextField(max_length=1500, default=None)
    watchers = models.IntegerField(default=0)
    goers = models.IntegerField(default=0)
    participants = models.IntegerField(default=0)
    level = models.CharField(max_length=10, default=None)
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['date_event']

    def __unicode__(self):
        return self.name