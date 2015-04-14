# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nominacoop', '0002_cuotasprestamosempresa_tipoprestamonomina'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuotasprestamosempresa',
            name='tipoPrestamoNomina',
        ),
        migrations.AddField(
            model_name='cuotasprestamosempresa',
            name='infoTipoPrestamo',
            field=models.CharField(default=b'0015', max_length=4),
            preserve_default=True,
        ),
    ]
