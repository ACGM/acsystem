# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0013_auto_20141231_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventarioh',
            name='diasPlazo',
            field=models.CharField(default=b'30', choices=[(b'30', b'30'), (b'60', b'60'), (b'120', b'120')], max_length=3, blank=True, null=True, verbose_name=b'Dias de Plazo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='inventarioh',
            name='nota',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
