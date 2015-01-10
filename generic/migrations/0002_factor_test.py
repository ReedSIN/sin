# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generic', '0001_squashed_0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='factor',
            name='test',
            field=models.CharField(default=b'hello world!', max_length=50),
            preserve_default=True,
        ),
    ]
