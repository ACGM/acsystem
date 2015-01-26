# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prestamos', '0004_solicitudprestamo_prestacioneslaborales'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudprestamo',
            name='salarioSocio',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
    ]
