# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prestamos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='maestraprestamo',
            name='quincenas',
            field=models.PositiveIntegerField(default=2),
            preserve_default=True,
        ),
    ]
