# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0004_auto_20150201_0315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='ordenCompra',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
