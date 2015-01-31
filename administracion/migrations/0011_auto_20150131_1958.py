# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0010_auto_20150131_1534'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuotaordenes',
            name='cantidadMeses',
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaInicioAhorro',
            field=models.DateField(default=datetime.datetime(2015, 1, 31, 19, 58, 20, 642403), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaModificacion',
            field=models.DateField(default=datetime.datetime(2015, 1, 31, 19, 58, 20, 642428), auto_now=True),
            preserve_default=True,
        ),
    ]
