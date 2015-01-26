# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prestamos', '0005_auto_20150125_0346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prestamounificado',
            name='capitalUnificado',
            field=models.DecimalField(max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
    ]
