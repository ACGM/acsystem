# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prestamos', '0003_auto_20150208_1539'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maestraprestamo',
            name='posteado',
        ),
        migrations.AddField(
            model_name='maestraprestamo',
            name='estatus',
            field=models.CharField(default=b'E', max_length=1),
            preserve_default=True,
        ),
    ]
