# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0011_auto_20141229_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventarioh',
            name='descripcionSalida',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Descripci\xc3\xb3n de Salida', blank=True),
            preserve_default=True,
        ),
    ]
