# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0002_auto_20150102_0712'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='end',
            field=models.DateTimeField(default=datetime.datetime(1994, 7, 29, 0, 0)),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(1994, 5, 29, 0, 0)),
            preserve_default=True,
        ),
    ]
