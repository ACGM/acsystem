# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0006_auto_20150226_0122'),
    ]

    operations = [
        migrations.AddField(
            model_name='representante',
            name='prueba',
            field=models.CharField(default=b's', max_length=1),
            preserve_default=True,
        ),
    ]
