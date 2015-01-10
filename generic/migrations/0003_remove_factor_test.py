# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generic', '0002_factor_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factor',
            name='test',
        ),
    ]
