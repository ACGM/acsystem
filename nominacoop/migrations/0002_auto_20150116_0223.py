# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nominacoop', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cuotasahorrosempresa',
            old_name='prueba',
            new_name='prueba2',
        ),
        migrations.RenameField(
            model_name='cuotasprestamosempresa',
            old_name='prueba',
            new_name='prueba34',
        ),
    ]
