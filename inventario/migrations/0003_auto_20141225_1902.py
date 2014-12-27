# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0002_auto_20141225_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventariod',
            name='cantidadFisico',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='inventariod',
            name='costo',
            field=models.DecimalField(null=True, max_digits=18, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
