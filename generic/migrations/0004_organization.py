# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generic', '0003_remove_factor_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=75)),
                ('website', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('meeting_info', models.TextField()),
                ('annual_events', models.TextField()),
                ('associated_off_campus_organizations', models.TextField()),
                ('enabled', models.BooleanField(default=True)),
                ('archived', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('signator', models.ForeignKey(related_name='signator_set', to='generic.SinUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
