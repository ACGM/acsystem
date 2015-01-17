# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nominacoop', '0008_auto_20150117_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargocoop',
            name='descripcion',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='empleadocoop',
            name='ciudad',
            field=models.CharField(max_length=40, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='empleadocoop',
            name='lugarNac',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Lugar de Nacimiento', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='empleadocoop',
            name='sector',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='empleadocoop',
            name='telefono',
            field=models.CharField(max_length=40, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tiponomina',
            name='descripcion',
            field=models.CharField(max_length=20),
            preserve_default=True,
        ),
    ]
