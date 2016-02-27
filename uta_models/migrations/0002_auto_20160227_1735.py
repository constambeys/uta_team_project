# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uta_models', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='students',
        ),
        migrations.AddField(
            model_name='assignment',
            name='students',
            field=models.ManyToManyField(to='uta_models.Student'),
            preserve_default=True,
        ),
    ]
