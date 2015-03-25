# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ahorro', '0004_retiroahorro_fecha'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='retiroahorro',
            name='ahorro',
        ),
    ]
