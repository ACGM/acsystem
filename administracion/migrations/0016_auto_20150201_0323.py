# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0015_auto_20150201_0315'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='bancoAsign',
            field=models.CharField(max_length=5, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaInicioAhorro',
            field=models.DateField(default=datetime.datetime(2015, 2, 1, 3, 23, 27, 496010), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaModificacion',
            field=models.DateField(default=datetime.datetime(2015, 2, 1, 3, 23, 27, 496034), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='empresa',
            name='rnc',
            field=models.CharField(max_length=15, null=True, blank=True),
            preserve_default=True,
        ),
    ]
