# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuenta', '0004_auto_20141213_0356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auxiliares',
            name='codigo',
            field=models.PositiveIntegerField(unique=True, verbose_name=b'C\xc3\xb3digo Auxiliar'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuentas',
            name='codigo',
            field=models.PositiveIntegerField(unique=True, verbose_name=b'C\xc3\xb3digo Cuenta'),
            preserve_default=True,
        ),
    ]
