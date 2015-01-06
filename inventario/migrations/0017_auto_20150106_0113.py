# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0016_auto_20150105_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='existencia',
            name='fecha',
            field=models.DateField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
