# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0004_banco_prueba'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banco',
            name='prueba',
        ),
    ]
