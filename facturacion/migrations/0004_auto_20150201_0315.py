# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0003_auto_20150201_0313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='ordenCompra',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
    ]
