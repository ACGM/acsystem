# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0017_auto_20150106_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='existencia',
            name='fecha',
            field=models.DateField(auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='existencia',
            name='producto',
            field=models.ForeignKey(to='administracion.Producto', unique=True),
            preserve_default=True,
        ),
    ]
