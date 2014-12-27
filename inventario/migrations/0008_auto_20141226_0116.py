# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '__first__'),
        ('inventario', '0007_remove_inventarioh_almacen'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventarioh',
            name='suplidor',
            field=models.ForeignKey(blank=True, to='administracion.Suplidor', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='inventarioh',
            name='ncf',
            field=models.CharField(max_length=25, verbose_name=b'NCF', blank=True),
            preserve_default=True,
        ),
    ]
