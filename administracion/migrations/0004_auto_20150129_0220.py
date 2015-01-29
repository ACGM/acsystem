# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0003_auto_20150129_0220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suplidor',
            name='prueba',
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaInicioAhorro',
            field=models.DateField(default=datetime.datetime(2015, 1, 29, 2, 20, 50, 566548), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaModificacion',
            field=models.DateField(default=datetime.datetime(2015, 1, 29, 2, 20, 50, 566574), auto_now=True),
            preserve_default=True,
        ),
    ]
