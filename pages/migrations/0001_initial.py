# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('domains', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('pageID', models.CharField(default=b'', unique=True, max_length=20)),
                ('description', models.CharField(default=b'', max_length=200)),
                ('memberNum', models.IntegerField(default=0)),
                ('admin', models.ForeignKey(to='users.User')),
                ('domain', models.ForeignKey(to='domains.Domain')),
            ],
        ),
    ]
