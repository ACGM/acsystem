# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0018_auto_20150107_0450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='existencia',
            name='producto',
            field=models.ForeignKey(to='administracion.Producto'),
            preserve_default=True,
        ),
    ]
