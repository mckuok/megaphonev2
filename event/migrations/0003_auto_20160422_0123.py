# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_event_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date_end',
            field=models.DateTimeField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_event',
            field=models.DateTimeField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(default=None, max_length=1500),
        ),
        migrations.AlterField(
            model_name='event',
            name='function',
            field=models.CharField(default=None, max_length=20),
        ),
        migrations.AlterField(
            model_name='event',
            name='level',
            field=models.CharField(default=None, max_length=10),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(default=None, max_length=30),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
