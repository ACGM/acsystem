# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prestamos', '0006_auto_20150126_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudprestamo',
            name='ahorrosCapitalizados',
            field=models.DecimalField(default=0, max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='solicitudprestamo',
            name='deudasPrestamos',
            field=models.DecimalField(default=0, max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
    ]
