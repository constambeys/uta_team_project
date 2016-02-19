# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uta_models', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('assignment', models.ForeignKey(to='uta_models.Assignment')),
                ('students', models.ManyToManyField(to='uta_models.Student')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
