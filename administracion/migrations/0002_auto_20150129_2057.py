# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaInicioAhorro',
            field=models.DateField(default=datetime.datetime(2015, 1, 29, 20, 57, 21, 773396), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaModificacion',
            field=models.DateField(default=datetime.datetime(2015, 1, 29, 20, 57, 21, 773421), auto_now=True),
            preserve_default=True,
        ),
    ]
