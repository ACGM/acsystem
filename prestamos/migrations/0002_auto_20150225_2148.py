# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prestamos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maestraprestamo',
            name='prueba',
        ),
        migrations.AddField(
            model_name='maestraprestamo',
            name='fechaAprobacion',
            field=models.DateField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
    ]
