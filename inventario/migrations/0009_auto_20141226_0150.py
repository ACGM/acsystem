# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0008_auto_20141226_0116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventarioh',
            name='posteo',
            field=models.CharField(default=b'N', max_length=1, choices=[(b'N', b'NO'), (b'S', b'SI')]),
            preserve_default=True,
        ),
    ]
