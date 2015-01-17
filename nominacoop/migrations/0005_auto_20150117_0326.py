# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nominacoop', '0004_remove_nominacoopd_userlog'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cargocoop',
            options={'ordering': ['descripcion'], 'verbose_name': 'Cargo Cooperativa', 'verbose_name_plural': 'Cargos Cooperativa'},
        ),
        migrations.AlterModelOptions(
            name='departamentocoop',
            options={'ordering': ['descripcion'], 'verbose_name': 'Departamento Cooperativa', 'verbose_name_plural': 'Departamentos Cooperativa'},
        ),
        migrations.AlterModelOptions(
            name='empleadocoop',
            options={'ordering': ['codigo'], 'verbose_name': 'Empleado Cooperativa', 'verbose_name_plural': 'Empleados Cooperativa'},
        ),
        migrations.AlterModelOptions(
            name='nominacoopd',
            options={'verbose_name': 'Nomina Detalles', 'verbose_name_plural': 'Nominas Detalles'},
        ),
        migrations.AlterModelOptions(
            name='nominacooph',
            options={'ordering': ['-fechaNomina'], 'verbose_name': 'Nomina Cabecera', 'verbose_name_plural': 'Nominas Cabecera'},
        ),
        migrations.AlterModelOptions(
            name='tiponomina',
            options={'ordering': ['descripcion'], 'verbose_name': 'Tipo de Nomina', 'verbose_name_plural': 'Tipos de Nominas'},
        ),
        migrations.AlterField(
            model_name='nominacooph',
            name='fechaNomina',
            field=models.DateField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='nominacooph',
            name='fechaPago',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
    ]
