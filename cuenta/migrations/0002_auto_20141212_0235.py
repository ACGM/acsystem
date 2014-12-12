# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuenta', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuentas',
            name='control',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='auxiliares',
            name='codigo',
            field=models.PositiveIntegerField(default=False, verbose_name=b'C\xc3\xb3digo Auxiliar'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuentas',
            name='codigo',
            field=models.PositiveIntegerField(default=False, verbose_name=b'C\xc3\xb3digo Cuenta'),
            preserve_default=True,
        ),
    ]
