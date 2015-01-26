# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prestamos', '0002_auto_20150121_2141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitudordendespachoh',
            name='descontar',
        ),
        migrations.RemoveField(
            model_name='solicitudordendespachoh',
            name='quincena',
        ),
        migrations.RemoveField(
            model_name='solicitudprestamo',
            name='descontar',
        ),
        migrations.RemoveField(
            model_name='solicitudprestamo',
            name='quincena',
        ),
        migrations.AddField(
            model_name='solicitudordendespachoh',
            name='prestamo',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='solicitudprestamo',
            name='prestamo',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
    ]
