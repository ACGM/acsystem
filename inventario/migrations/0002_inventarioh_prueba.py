# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventarioh',
            name='prueba',
            field=models.CharField(max_length=1, null=True, blank=True),
            preserve_default=True,
        ),
    ]
