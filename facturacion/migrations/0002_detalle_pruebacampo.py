# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalle',
            name='pruebacampo',
            field=models.PositiveIntegerField(default=1),
            preserve_default=True,
        ),
    ]
