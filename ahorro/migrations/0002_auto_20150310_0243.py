# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ahorro', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maestraahorro',
            name='estatus',
            field=models.CharField(max_length=1, verbose_name=b'Estatus', choices=[(b'A', b'Activas'), (b'I', b'Inactivas'), (b'P', b'Posteada')]),
            preserve_default=True,
        ),
    ]
