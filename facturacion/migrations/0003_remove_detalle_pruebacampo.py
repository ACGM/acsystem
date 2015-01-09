# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0002_detalle_pruebacampo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detalle',
            name='pruebacampo',
        ),
    ]
