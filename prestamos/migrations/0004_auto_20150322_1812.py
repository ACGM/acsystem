# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prestamos', '0003_maestraprestamo_tiponomina'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maestraprestamo',
            name='tipoNomina',
        ),
        migrations.AddField(
            model_name='maestraprestamo',
            name='tipoPrestamoNomina',
            field=models.CharField(default=b'RE', max_length=2, choices=[(b'RE', b'Regular'), (b'BO', b'Bonificacion'), (b'RG', b'Regalia'), (b'VA', b'Vacaciones'), (b'RI', b'Rifa')]),
            preserve_default=True,
        ),
    ]
