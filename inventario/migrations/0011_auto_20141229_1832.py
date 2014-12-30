# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0010_auto_20141229_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventarioh',
            name='factura',
            field=models.CharField(max_length=12, null=True, blank=True),
            preserve_default=True,
        ),
    ]
