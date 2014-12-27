# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventarioh',
            name='factura',
            field=models.CharField(max_length=30, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='inventarioh',
            name='orden',
            field=models.CharField(max_length=30, null=True, blank=True),
            preserve_default=True,
        ),
    ]
