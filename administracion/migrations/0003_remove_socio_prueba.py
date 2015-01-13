# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0002_socio_prueba'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socio',
            name='prueba',
        ),
    ]
