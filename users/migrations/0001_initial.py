# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(unique=True, max_length=20)),
                ('role', models.CharField(max_length=20)),
                ('date_joined', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('subscribe_domain', models.CharField(default=b'', max_length=300, blank=True)),
                ('subscribe_page', models.CharField(default=b'', max_length=300, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
