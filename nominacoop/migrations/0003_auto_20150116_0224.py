# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nominacoop', '0002_auto_20150116_0223'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuotasahorrosempresa',
            name='prueba2',
        ),
        migrations.RemoveField(
            model_name='cuotasprestamosempresa',
            name='prueba34',
        ),
    ]
