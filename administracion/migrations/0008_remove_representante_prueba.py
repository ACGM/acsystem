# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0007_representante_prueba'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='representante',
            name='prueba',
        ),
    ]
