# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0002_auto_20150101_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socio',
            name='apellidos',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socio',
            name='celular',
            field=models.CharField(max_length=80, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socio',
            name='ciudad',
            field=models.CharField(max_length=80, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socio',
            name='nombres',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socio',
            name='sector',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socio',
            name='telefono',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
    ]
