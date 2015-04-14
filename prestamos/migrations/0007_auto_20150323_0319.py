# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prestamos', '0006_auto_20150323_0318'),
    ]

    operations = [
        migrations.AddField(
            model_name='maestraprestamo',
            name='montoCuotaQ1',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='maestraprestamo',
            name='montoCuotaQ2',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
