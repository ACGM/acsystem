# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nominacoop', '0004_nominaprestamosahorros_infotipo'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cuotasprestamosempresa',
            unique_together=set([('noPrestamo', 'nomina')]),
        ),
    ]
