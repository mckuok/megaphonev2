# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0002_auto_20160418_0530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domain',
            name='description',
            field=models.TextField(default=b'', max_length=200),
        ),
    ]
