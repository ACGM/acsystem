# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0008_auto_20150130_0449'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='rnc',
            field=models.CharField(default=b'', max_length=15, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaInicioAhorro',
            field=models.DateField(default=datetime.datetime(2015, 1, 31, 0, 36, 43, 498177), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaModificacion',
            field=models.DateField(default=datetime.datetime(2015, 1, 31, 0, 36, 43, 498203), auto_now=True),
            preserve_default=True,
        ),
    ]
