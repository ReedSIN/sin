# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factor',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID',
                    serialize=False,
                    auto_created=True,
                    primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={},
            bases=(models.Model, ), ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID',
                    serialize=False,
                    auto_created=True,
                    primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=75)),
                ('website', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('meeting_info', models.TextField()),
                ('annual_events', models.TextField()),
                ('associated_off_campus_organizations', models.TextField()),
                ('public_post_ok', models.BooleanField(default=False)),
                ('referral_info', models.TextField()),
                ('enabled', models.BooleanField(default=True)),
                ('archived', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
            ],
            options={},
            bases=(models.Model, ), ),
        migrations.CreateModel(
            name='SinUser',
            fields=[
                ('user_ptr', models.OneToOneField(
                    parent_link=True,
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    to=settings.AUTH_USER_MODEL)),
                ('attended_signator_training', models.BooleanField(
                    default=False)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user', ), ),
        migrations.AddField(
            model_name='organization',
            name='signator',
            field=models.ForeignKey(
                related_name='signator_set', to='generic.SinUser'),
            preserve_default=True, ),
        migrations.AddField(
            model_name='factor',
            name='users',
            field=models.ManyToManyField(to='generic.SinUser'),
            preserve_default=True, ),
    ]
