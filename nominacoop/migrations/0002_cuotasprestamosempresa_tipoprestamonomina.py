# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nominacoop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuotasprestamosempresa',
            name='tipoPrestamoNomina',
            field=models.CharField(default=b'RE', max_length=2),
            preserve_default=True,
        ),
    ]
