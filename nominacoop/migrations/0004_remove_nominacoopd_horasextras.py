# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nominacoop', '0003_remove_nominacoopd_prueba'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nominacoopd',
            name='horasExtras',
        ),
    ]
