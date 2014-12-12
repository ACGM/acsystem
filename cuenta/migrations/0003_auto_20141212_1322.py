# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuenta', '0002_auto_20141212_0235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuentas',
            name='descripcion',
            field=models.CharField(max_length=100, verbose_name=b'Descripcion'),
            preserve_default=True,
        ),
    ]
