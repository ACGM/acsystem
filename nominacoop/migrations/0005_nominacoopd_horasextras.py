# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nominacoop', '0004_remove_nominacoopd_horasextras'),
    ]

    operations = [
        migrations.AddField(
            model_name='nominacoopd',
            name='horasExtras',
            field=models.DecimalField(default=0, null=True, max_digits=12, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
