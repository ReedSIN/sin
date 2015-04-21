# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0003_auto_20150412_0048'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='writeInOption',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
