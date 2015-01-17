# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nominacoop', '0006_auto_20150117_0523'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tiponomina',
            options={'ordering': ['id'], 'verbose_name': 'Tipo de Nomina', 'verbose_name_plural': 'Tipos de Nominas'},
        ),
        migrations.AlterField(
            model_name='empleadocoop',
            name='codigo',
            field=models.PositiveIntegerField(max_length=6),
            preserve_default=True,
        ),
    ]
