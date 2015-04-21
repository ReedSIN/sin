# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0004_election_writeinoption'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='blurb',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
