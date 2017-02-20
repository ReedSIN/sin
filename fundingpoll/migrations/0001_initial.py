# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='FundingPoll',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID',
                    serialize=False,
                    auto_created=True,
                    primary_key=True)),
                ('start_registration', models.DateTimeField()),
                ('end_registration', models.DateTimeField()),
                ('start_voting', models.DateTimeField()),
                ('end_voting', models.DateTimeField()),
                ('start_budgets', models.DateTimeField()),
                ('end_budgets', models.DateTimeField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
            ],
            options={},
            bases=(models.Model, ), ),
        migrations.CreateModel(
            name='FundingPollBudget',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID',
                    serialize=False,
                    auto_created=True,
                    primary_key=True)),
                ('description', models.TextField()),
                ('response', models.TextField()),
                ('requested', models.DecimalField(
                    max_digits=8, decimal_places=2)),
                ('allocated', models.DecimalField(
                    max_digits=8, decimal_places=2)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
            ],
            options={},
            bases=(models.Model, ), ),
        migrations.CreateModel(
            name='FundingPollBudgetItem',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID',
                    serialize=False,
                    auto_created=True,
                    primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('response', models.TextField()),
                ('requested', models.DecimalField(
                    max_digits=8, decimal_places=2)),
                ('allocated', models.DecimalField(
                    max_digits=8, decimal_places=2)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
            ],
            options={},
            bases=(models.Model, ), ),
        migrations.CreateModel(
            name='FundingPollOrganization',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID',
                    serialize=False,
                    auto_created=True,
                    primary_key=True)),
                ('other_signators', models.CharField(max_length=50)),
                ('comment', models.TextField()),
                ('total_votes', models.IntegerField()),
                ('top_six', models.IntegerField()),
                ('approve', models.IntegerField()),
                ('no_opinion', models.IntegerField()),
                ('disapprove', models.IntegerField()),
                ('deep_six', models.IntegerField()),
                ('ordering', models.FloatField(default=0.0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
            ],
            options={},
            bases=(models.Model, ), ),
        migrations.CreateModel(
            name='FundingPollVote',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID',
                    serialize=False,
                    auto_created=True,
                    primary_key=True)),
                ('scalar', models.IntegerField(choices=[(8, b'Top Six'),
                                                        (2, b'Approve'),
                                                        (0, b'No Opinion'),
                                                        (-1, b'Disapprove'),
                                                        (-4, b'Deep Six')])),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('funding_poll', models.ForeignKey(
                    to='fundingpoll.FundingPoll')),
                ('organization', models.ForeignKey(
                    to='fundingpoll.FundingPollOrganization')),
            ],
            options={},
            bases=(models.Model, ), ),
    ]
