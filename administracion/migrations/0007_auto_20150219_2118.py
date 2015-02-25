# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0006_auto_20150219_0451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socio',
            name='cuotaAhorroQ1',
            field=models.DecimalField(default=0, verbose_name=b'Cuota Ahorro Q1', max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socio',
            name='cuotaAhorroQ2',
            field=models.DecimalField(default=0, verbose_name=b'Cuota Ahorro Q2', max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
    ]
