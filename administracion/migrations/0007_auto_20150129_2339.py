# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0006_auto_20150129_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaInicioAhorro',
            field=models.DateField(default=datetime.datetime(2015, 1, 29, 23, 39, 36, 663794), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaModificacion',
            field=models.DateField(default=datetime.datetime(2015, 1, 29, 23, 39, 36, 663823), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='producto',
            unique_together=set([]),
        ),
    ]
