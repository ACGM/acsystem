# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0002_existencia_cantidadanterior'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventarioh',
            name='diasPlazo',
            field=models.CharField(max_length=3, null=True, verbose_name=b'Dias de Plazo', blank=True),
            preserve_default=True,
        ),
    ]
