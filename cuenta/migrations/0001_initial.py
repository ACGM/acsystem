# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auxiliares',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.PositiveIntegerField(unique=True, verbose_name=b'C\xc3\xb3digo Auxiliar')),
                ('descripcion', models.CharField(max_length=200, verbose_name=b'Descripcion')),
            ],
            options={
                'ordering': ['codigo'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cuentas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.PositiveIntegerField(unique=True, verbose_name=b'C\xc3\xb3digo Cuenta')),
                ('descripcion', models.CharField(max_length=100, verbose_name=b'Descripcion')),
                ('origen', models.CharField(max_length=1, verbose_name=b'Origen de la cuenta', choices=[(b'D', b'Debito'), (b'C', b'Credito')])),
                ('control', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['codigo'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CuentasControl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigoControl', models.PositiveIntegerField(unique=True, verbose_name=b'Cuenta control')),
                ('descripcion', models.CharField(max_length=100, verbose_name=b'Descripcion')),
            ],
            options={
                'ordering': ['codigoControl'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DiarioGeneral',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('referencia', models.CharField(max_length=30, verbose_name=b'Ref')),
                ('estatus', models.CharField(default=b'R', max_length=1, choices=[(b'P', b'Posteada'), (b'R', b'Registrada'), (b'C', b'Cancelada')])),
                ('debito', models.DecimalField(verbose_name=b'Debito', max_digits=18, decimal_places=2)),
                ('credito', models.DecimalField(verbose_name=b'Credito', max_digits=18, decimal_places=2)),
                ('auxiliar', models.ForeignKey(verbose_name=b'Aux', blank=True, to='cuenta.Auxiliares', null=True)),
                ('cuenta', models.ForeignKey(verbose_name=b'Cuenta', blank=True, to='cuenta.Cuentas', null=True)),
            ],
            options={
                'ordering': ['fecha'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoDocumento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipoDoc', models.CharField(unique=True, max_length=4, verbose_name=b'Tipo de Documento')),
                ('descripcion', models.CharField(max_length=100, verbose_name=b'Descripcion')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='diariogeneral',
            name='tipoDoc',
            field=models.ForeignKey(to='cuenta.TipoDocumento'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cuentas',
            name='cuentaControl',
            field=models.ForeignKey(blank=True, to='cuenta.CuentasControl', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='auxiliares',
            name='cuenta',
            field=models.ForeignKey(verbose_name=b'Cuenta', to='cuenta.Cuentas'),
            preserve_default=True,
        ),
    ]
