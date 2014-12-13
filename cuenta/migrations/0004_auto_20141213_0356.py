# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuenta', '0003_auto_20141212_1322'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='auxiliares',
            options={'ordering': ['codigo']},
        ),
        migrations.AlterModelOptions(
            name='diariogeneral',
            options={'ordering': ['fecha']},
        ),
        migrations.AlterField(
            model_name='auxiliares',
            name='codigo',
            field=models.PositiveIntegerField(verbose_name=b'C\xc3\xb3digo Auxiliar'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuentas',
            name='codigo',
            field=models.PositiveIntegerField(verbose_name=b'C\xc3\xb3digo Cuenta'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuentas',
            name='cuentaControl',
            field=models.PositiveIntegerField(null=True, verbose_name=b'Cuenta Control', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='diariogeneral',
            name='referencia',
            field=models.PositiveIntegerField(verbose_name=b'Ref'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='diariogeneral',
            name='tipoDoc',
            field=models.CharField(max_length=3, verbose_name=b'Tipo de Doc'),
            preserve_default=True,
        ),
    ]
