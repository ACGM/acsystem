# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0003_auto_20150105_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socio',
            name='carnetNumero',
            field=models.PositiveIntegerField(verbose_name=b'Carnet Numero'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socio',
            name='codigo',
            field=models.PositiveIntegerField(),
            preserve_default=True,
        ),
    ]
