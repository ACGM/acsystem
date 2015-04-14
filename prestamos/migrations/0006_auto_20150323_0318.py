# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prestamos', '0005_auto_20150322_1923'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maestraprestamo',
            name='montoCuotaQ1',
        ),
        migrations.RemoveField(
            model_name='maestraprestamo',
            name='montoCuotaQ2',
        ),
    ]
