# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nominacoop', '0005_auto_20150325_2242'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='nominaprestamosahorros',
            unique_together=set([('nomina', 'infoTipo')]),
        ),
    ]
