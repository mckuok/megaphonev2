# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=50)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_event', models.DateTimeField(null=True, blank=True)),
                ('date_end', models.DateTimeField(null=True, blank=True)),
                ('location', models.CharField(default=b'', max_length=30)),
                ('function', models.CharField(default=b'', max_length=20)),
                ('description', models.TextField(default=b'', max_length=1500)),
                ('watchers', models.IntegerField(default=0)),
                ('goers', models.IntegerField(default=0)),
                ('participants', models.IntegerField(default=0)),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'ordering': ['date_event'],
            },
        ),
    ]
