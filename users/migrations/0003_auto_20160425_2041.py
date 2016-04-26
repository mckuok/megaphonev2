# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_last_access'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='checked_announcement',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='checked_event',
            field=models.BooleanField(default=False),
        ),
    ]
