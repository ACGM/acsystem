# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0002_auto_20150131_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='descrpAnulacion',
            field=models.CharField(max_length=150, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='factura',
            name='ordenCompra',
            field=models.PositiveIntegerField(default=0, null=True),
            preserve_default=True,
        ),
    ]
