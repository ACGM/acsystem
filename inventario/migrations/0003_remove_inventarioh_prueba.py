# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0002_inventarioh_prueba'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventarioh',
            name='prueba',
        ),
    ]
