# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0005_auto_20150119_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaInicioAhorro',
            field=models.DateField(default=datetime.datetime(2015, 1, 21, 21, 41, 34, 971556), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaModificacion',
            field=models.DateField(default=datetime.datetime(2015, 1, 21, 21, 41, 34, 971600), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='representante',
            name='nombre',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socio',
            name='codigo',
            field=models.PositiveIntegerField(),
            preserve_default=True,
        ),
    ]
