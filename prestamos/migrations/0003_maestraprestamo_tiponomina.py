# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prestamos', '0002_maestraprestamo_quincenas'),
    ]

    operations = [
        migrations.AddField(
            model_name='maestraprestamo',
            name='tipoNomina',
            field=models.CharField(default=b'Regular', max_length=15),
            preserve_default=True,
        ),
    ]
