# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prestamos', '0004_auto_20150322_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maestraprestamo',
            name='posteadoFecha',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
    ]
