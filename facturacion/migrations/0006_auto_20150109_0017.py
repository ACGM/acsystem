# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0005_auto_20150108_0516'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordendespachosupercoop',
            name='id',
        ),
        migrations.AlterField(
            model_name='ordendespachosupercoop',
            name='noSolicitud',
            field=models.AutoField(serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
