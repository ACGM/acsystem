# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ahorro', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='retiroahorro',
            name='socio',
            field=models.ForeignKey(default=1, to='administracion.Socio'),
            preserve_default=False,
        ),
    ]
