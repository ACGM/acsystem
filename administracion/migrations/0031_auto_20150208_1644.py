# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0030_auto_20150208_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaInicioAhorro',
            field=models.DateField(default=datetime.datetime(2015, 2, 8, 16, 44, 9, 648888), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaModificacion',
            field=models.DateField(default=datetime.datetime(2015, 2, 8, 16, 44, 9, 648910), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='distrito',
            name='descripcion',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
    ]
