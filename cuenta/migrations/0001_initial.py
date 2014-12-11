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
                ('codigo', models.PositiveIntegerField(default=False, verbose_name=b'Codigo Auxiliar')),
                ('descripcion', models.CharField(max_length=200, verbose_name=b'Descripcion')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cuentas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.PositiveIntegerField(default=False, verbose_name=b'Codigo Cuenta')),
                ('descripcion', models.CharField(max_length=255, verbose_name=b'Descripcion')),
                ('origen', models.CharField(max_length=1, verbose_name=b'Origen de la cuenta', choices=[(b'D', b'Debito'), (b'C', b'Credito')])),
                ('cuentaControl', models.PositiveIntegerField(default=False, null=True, verbose_name=b'Cuenta Control', blank=True)),
            ],
            options={
                'ordering': ['codigo'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DiarioGeneral',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField()),
                ('referencia', models.PositiveIntegerField(default=False, verbose_name=b'Ref')),
                ('tipoDoc', models.CharField(default=False, max_length=3, verbose_name=b'Tipo de Doc')),
                ('debito', models.DecimalField(verbose_name=b'Debito', max_digits=18, decimal_places=2)),
                ('Credito', models.DecimalField(verbose_name=b'Credito', max_digits=18, decimal_places=2)),
                ('auxiliar', models.ForeignKey(verbose_name=b'Aux', blank=True, to='cuenta.Auxiliares', null=True)),
                ('cuenta', models.ForeignKey(verbose_name=b'Cuenta', blank=True, to='cuenta.Cuentas', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='auxiliares',
            name='cuenta',
            field=models.ForeignKey(verbose_name=b'Cuenta', to='cuenta.Cuentas'),
            preserve_default=True,
        ),
    ]
