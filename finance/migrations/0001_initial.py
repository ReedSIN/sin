# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generic', '0004_organization'),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField()),
                ('reponse', models.TextField()),
                ('requested', models.DecimalField(max_digits=8, decimal_places=2)),
                ('allocated', models.DecimalField(max_digits=8, decimal_places=2)),
                ('claimed', models.DecimalField(max_digits=8, decimal_places=2)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('finalized', models.IntegerField(default=0)),
                ('approved', models.IntegerField(default=0)),
                ('organization', models.ForeignKey(to='generic.Organization')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BudgetItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('response', models.TextField()),
                ('requested', models.DecimalField(max_digits=8, decimal_places=2)),
                ('allocated', models.DecimalField(max_digits=8, decimal_places=2)),
                ('claimed', models.DecimalField(max_digits=8, decimal_places=2)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('budget', models.ForeignKey(to='finance.Budget')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
