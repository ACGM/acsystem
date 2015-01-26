# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0009_auto_20150123_2206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuotaprestamo',
            name='cantidadMeses',
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaInicioAhorro',
            field=models.DateField(default=datetime.datetime(2015, 1, 23, 23, 4, 47, 522240), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaModificacion',
            field=models.DateField(default=datetime.datetime(2015, 1, 23, 23, 4, 47, 522265), auto_now=True),
            preserve_default=True,
        ),
    ]
