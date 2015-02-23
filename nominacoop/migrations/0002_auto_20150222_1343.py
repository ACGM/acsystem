# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prestamos', '0001_initial'),
        ('nominacoop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuotasprestamosempresa',
            name='prueba',
        ),
        migrations.AddField(
            model_name='cuotasprestamosempresa',
            name='cuota',
            field=models.ForeignKey(to='prestamos.PagoCuotasPrestamo', null=True),
            preserve_default=True,
        ),
    ]
