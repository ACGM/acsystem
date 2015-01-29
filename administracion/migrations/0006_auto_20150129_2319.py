# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0005_auto_20150129_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaInicioAhorro',
            field=models.DateField(default=datetime.datetime(2015, 1, 29, 23, 19, 40, 535041), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaModificacion',
            field=models.DateField(default=datetime.datetime(2015, 1, 29, 23, 19, 40, 535067), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='producto',
            name='codigo',
            field=models.CharField(max_length=10, editable=False),
            preserve_default=True,
        ),
    ]
