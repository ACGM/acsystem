# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0012_auto_20141230_0439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='almacen',
            name='descripcion',
            field=models.CharField(max_length=20),
            preserve_default=True,
        ),
    ]
