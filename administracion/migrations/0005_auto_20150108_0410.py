# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0004_auto_20150106_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departamento',
            name='descripcion',
            field=models.CharField(max_length=80),
            preserve_default=True,
        ),
    ]
