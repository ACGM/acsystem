# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0005_remove_movimiento_prueba'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventarioh',
            name='posteo',
            field=models.CharField(default=b'N', max_length=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='inventarioh',
            name='diasPlazo',
            field=models.CharField(default=b'30', max_length=3, verbose_name=b'Dias de Plazo', choices=[(b'30', b'30'), (b'60', b'60'), (b'120', b'120')]),
            preserve_default=True,
        ),
    ]
