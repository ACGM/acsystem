# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0007_auto_20150109_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoriaprestamo',
            name='descripcion',
            field=models.CharField(max_length=70),
            preserve_default=True,
        ),
    ]
