from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class Announcement(models.Model):
    date_created = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=60, default="")
    text = models.CharField(max_length=1000)
    level = models.CharField(max_length=10, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-date_created']

    def __unicode__(self):
        return self.text
