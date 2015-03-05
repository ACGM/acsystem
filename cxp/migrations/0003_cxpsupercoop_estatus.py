# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cxp', '0002_remove_cxpsupercoop_estatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='cxpsupercoop',
            name='estatus',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
