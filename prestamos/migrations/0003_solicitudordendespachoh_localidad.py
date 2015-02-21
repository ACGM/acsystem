# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0007_auto_20150219_2118'),
        ('prestamos', '0002_solicitudprestamo_localidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudordendespachoh',
            name='localidad',
            field=models.ForeignKey(blank=True, to='administracion.Localidad', null=True),
            preserve_default=True,
        ),
    ]
