# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cxp', '0006_remove_detalleorden_orden'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalleorden',
            name='orden',
            field=models.PositiveIntegerField(default=1, verbose_name=b'Orden'),
            preserve_default=False,
        ),
    ]
