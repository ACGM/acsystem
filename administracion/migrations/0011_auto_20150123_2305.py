# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0010_auto_20150123_2304'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cuotaprestamo',
            old_name='user',
            new_name='userLog',
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaInicioAhorro',
            field=models.DateField(default=datetime.datetime(2015, 1, 23, 23, 5, 45, 878009), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaModificacion',
            field=models.DateField(default=datetime.datetime(2015, 1, 23, 23, 5, 45, 878033), auto_now=True),
            preserve_default=True,
        ),
    ]
