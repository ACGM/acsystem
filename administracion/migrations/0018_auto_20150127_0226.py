# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0017_auto_20150127_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cobrador',
            name='userLog',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaInicioAhorro',
            field=models.DateField(default=datetime.datetime(2015, 1, 27, 2, 26, 28, 905376), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaModificacion',
            field=models.DateField(default=datetime.datetime(2015, 1, 27, 2, 26, 28, 905399), auto_now=True),
            preserve_default=True,
        ),
    ]
