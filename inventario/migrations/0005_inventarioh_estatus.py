# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0004_auto_20150203_0117'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventarioh',
            name='estatus',
            field=models.CharField(default=b'E', max_length=1, choices=[(b'E', b'Entrada'), (b'S', b'Salida')]),
            preserve_default=True,
        ),
    ]
