# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0002_auto_20150129_0218'),
    ]

    operations = [
        migrations.AddField(
            model_name='suplidor',
            name='prueba',
            field=models.CharField(default=b'H', max_length=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaInicioAhorro',
            field=models.DateField(default=datetime.datetime(2015, 1, 29, 2, 20, 25, 323550), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaModificacion',
            field=models.DateField(default=datetime.datetime(2015, 1, 29, 2, 20, 25, 323575), auto_now=True),
            preserve_default=True,
        ),
    ]
