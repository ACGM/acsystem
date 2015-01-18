# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nominacoop', '0007_auto_20150117_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departamentocoop',
            name='descripcion',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
    ]
