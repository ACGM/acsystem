# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nominacoop', '0010_auto_20150117_1553'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nominacooph',
            options={'ordering': ['-id'], 'verbose_name': 'Nomina Cabecera', 'verbose_name_plural': 'Nominas Cabecera'},
        ),
    ]
