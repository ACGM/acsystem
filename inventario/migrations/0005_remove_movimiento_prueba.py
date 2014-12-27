# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0004_auto_20141225_2338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movimiento',
            name='prueba',
        ),
    ]
