# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prestamos', '0004_auto_20150208_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maestraprestamo',
            name='estatus',
            field=models.CharField(default=b'E', max_length=1, choices=[(b'E', b'En proceso'), (b'P', b'Posteado'), (b'S', b'Saldado')]),
            preserve_default=True,
        ),
    ]
