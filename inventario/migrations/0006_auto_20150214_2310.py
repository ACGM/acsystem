# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0005_auto_20150214_2218'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ajusteinventarioh',
            options={'ordering': ('id',)},
        ),
        migrations.AddField(
            model_name='ajusteinventarioh',
            name='estatus',
            field=models.CharField(default=b'E', max_length=1),
            preserve_default=True,
        ),
    ]
