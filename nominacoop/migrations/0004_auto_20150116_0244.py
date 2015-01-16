# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nominacoop', '0003_auto_20150116_0224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleadocoop',
            name='apellidos',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='empleadocoop',
            name='nombres',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
    ]
