# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nominacoop', '0002_auto_20150222_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuotasprestamosempresa',
            name='cuota',
            field=models.ForeignKey(to='prestamos.PagoCuotasPrestamo'),
            preserve_default=True,
        ),
    ]
