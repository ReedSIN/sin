# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID',
                    serialize=False,
                    auto_created=True,
                    primary_key=True)),
                ('preferred_pron', models.CharField(max_length=10,
                                                    blank=True)),
                ('major', models.CharField(max_length=30)),
                ('year', models.IntegerField(
                    max_length=1,
                    choices=[(0, b'Freshman'), (1, b'Sophomore'), (
                        2, b'Junior'), (3, b'Senior')])),
                ('address', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=75)),
                ('schedule_conflicts', models.TextField()),
                ('other_reed_positions', models.TextField()),
                ('other_employment', models.TextField()),
                ('experience', models.TextField()),
                ('motivation', models.TextField()),
                ('special_skills', models.TextField()),
                ('appeal', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
            ],
            options={},
            bases=(models.Model, ), ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID',
                    serialize=False,
                    auto_created=True,
                    primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('expires_on', models.DateTimeField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
            ],
            options={},
            bases=(models.Model, ), ),
    ]
