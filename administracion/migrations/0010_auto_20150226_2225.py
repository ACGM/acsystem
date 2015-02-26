# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0009_empresa_correoheader'),
    ]

    operations = [
        migrations.AddField(
            model_name='suplidor',
            name='cuentaBancaria',
            field=models.CharField(max_length=20, null=True, verbose_name=b'Cuenta Bancaria', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='suplidor',
            name='sexo',
            field=models.CharField(default=b'M', max_length=1, choices=[(b'M', b'Masculino'), (b'F', b'Femenino')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='suplidor',
            name='tipoCuentaBancaria',
            field=models.CharField(max_length=2, null=True, verbose_name=b'Tipo Cuenta Bancaria', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='suplidor',
            name='tipoIdentificacion',
            field=models.CharField(default=b'C', max_length=1, verbose_name=b'Tipo de Identificacion', choices=[(b'CE', b'Cedula'), (b'RN', b'RNC')]),
            preserve_default=True,
        ),
    ]
