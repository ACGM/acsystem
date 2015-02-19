# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0006_auto_20150214_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventarioh',
            name='numeroSalida',
            field=models.PositiveIntegerField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transferenciasalmacenes',
            name='fechaTransf',
            field=models.DateField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
