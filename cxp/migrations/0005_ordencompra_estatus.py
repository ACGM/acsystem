# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cxp', '0004_remove_ordencompra_estatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordencompra',
            name='estatus',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
