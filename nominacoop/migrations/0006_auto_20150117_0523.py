# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nominacoop', '0005_auto_20150117_0326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nominacooph',
            name='valorNomina',
        ),
        migrations.AlterField(
            model_name='nominacoopd',
            name='afp',
            field=models.DecimalField(default=0, null=True, max_digits=18, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='nominacoopd',
            name='ars',
            field=models.DecimalField(default=0, null=True, max_digits=18, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='nominacoopd',
            name='cafeteria',
            field=models.DecimalField(default=0, null=True, max_digits=18, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='nominacoopd',
            name='descAhorros',
            field=models.DecimalField(default=0, null=True, max_digits=18, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='nominacoopd',
            name='descPrestamos',
            field=models.DecimalField(default=0, null=True, max_digits=18, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='nominacoopd',
            name='isr',
            field=models.DecimalField(default=0, null=True, max_digits=18, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='nominacoopd',
            name='otrosIngresos',
            field=models.DecimalField(default=0, null=True, max_digits=18, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='nominacoopd',
            name='vacaciones',
            field=models.DecimalField(default=0, null=True, max_digits=18, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='nominacooph',
            name='quincena',
            field=models.PositiveIntegerField(default=1, choices=[(1, b'1ra. Quincena'), (2, b'2da. Quincena')]),
            preserve_default=True,
        ),
    ]
