# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0015_auto_20150105_0352'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inventarioh',
            options={'ordering': ('-id',), 'verbose_name': 'Inventario Cabecera', 'verbose_name_plural': 'Inventario Cabecera'},
        ),
    ]
