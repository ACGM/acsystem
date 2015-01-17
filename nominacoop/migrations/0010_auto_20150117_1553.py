# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nominacoop', '0009_auto_20150117_1455'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='nominacooph',
            unique_together=set([('fechaNomina', 'tipoNomina')]),
        ),
    ]
