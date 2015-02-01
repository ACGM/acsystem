# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0017_auto_20150201_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autorizador',
            name='clave',
            field=models.CharField(max_length=4),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaInicioAhorro',
            field=models.DateField(default=datetime.datetime(2015, 2, 1, 21, 3, 56, 942011), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaModificacion',
            field=models.DateField(default=datetime.datetime(2015, 2, 1, 21, 3, 56, 942034), auto_now=True),
            preserve_default=True,
        ),
    ]
