# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0014_auto_20150101_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventarioh',
            name='condicion',
            field=models.CharField(default=b'CO', max_length=2, choices=[(b'CO', b'Contado'), (b'CR', b'Credito')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='inventarioh',
            name='ncf',
            field=models.CharField(max_length=25, null=True, verbose_name=b'NCF', blank=True),
            preserve_default=True,
        ),
    ]
