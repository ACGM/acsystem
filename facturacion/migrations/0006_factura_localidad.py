# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0027_auto_20150206_1934'),
        ('facturacion', '0005_auto_20150201_0315'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='localidad',
            field=models.ForeignKey(to='administracion.Localidad', null=True),
            preserve_default=True,
        ),
    ]
