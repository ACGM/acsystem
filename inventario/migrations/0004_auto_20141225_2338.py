# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0003_auto_20141225_1902'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inventariod',
            options={'verbose_name': 'Inventario Detalle', 'verbose_name_plural': 'Inventario Detalle'},
        ),
        migrations.AlterModelOptions(
            name='inventarioh',
            options={'verbose_name': 'Inventario Cabecera', 'verbose_name_plural': 'Inventario Cabecera'},
        ),
        migrations.AddField(
            model_name='movimiento',
            name='prueba',
            field=models.CharField(default=b'HOLA', max_length=10),
            preserve_default=True,
        ),
    ]
