# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Ballot',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID',
                    serialize=False,
                    auto_created=True,
                    primary_key=True)),
                ('quorum', models.BooleanField(default=False)),
                ('votes', models.CommaSeparatedIntegerField(max_length=150)),
            ],
            options={},
            bases=(models.Model, ), ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID',
                    serialize=False,
                    auto_created=True,
                    primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('blurb', models.TextField(default=b'')),
                ('write_in', models.BooleanField(default=False)),
            ],
            options={},
            bases=(models.Model, ), ),
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID',
                    serialize=False,
                    auto_created=True,
                    primary_key=True)),
                ('position', models.CharField(max_length=50)),
                ('numSeats', models.IntegerField(default=1)),
                ('quorumOption', models.BooleanField(default=True)),
                ('writeInOption', models.BooleanField(default=True)),
                ('start', models.DateTimeField(default=datetime.datetime(
                    1994, 5, 29, 0, 0))),
                ('end', models.DateTimeField(default=datetime.datetime(
                    1994, 7, 29, 0, 0))),
            ],
            options={},
            bases=(models.Model, ), ),
        migrations.AddField(
            model_name='candidate',
            name='election',
            field=models.ForeignKey(
                related_name='candidate_set', to='elections.Election'),
            preserve_default=True, ),
        migrations.AddField(
            model_name='ballot',
            name='election',
            field=models.ForeignKey(
                related_name='ballot_set', to='elections.Election'),
            preserve_default=True, ),
    ]
