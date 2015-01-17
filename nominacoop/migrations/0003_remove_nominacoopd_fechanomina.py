# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nominacoop', '0002_auto_20150117_0031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nominacoopd',
            name='fechaNomina',
        ),
    ]
