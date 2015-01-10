# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ballot',
            name='quorum',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
