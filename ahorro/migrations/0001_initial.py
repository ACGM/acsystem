# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuenta', '0004_auto_20141213_0356'),
        ('administracion', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='AhorroSocio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('balance', models.DecimalField(verbose_name=b'Balance Socio', max_digits=18, decimal_places=2)),
                ('disponible', models.DecimalField(verbose_name=b'Disponible', max_digits=18, decimal_places=2)),
                ('beneficiario', models.ForeignKey(blank=True, to='administracion.CoBeneficiario', null=True)),
                ('socio', models.ForeignKey(null=True, blank=True, to='administracion.Socio', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DetalleCuentaMaestraAhorro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('debito', models.DecimalField(default=0.0, verbose_name=b'Debito', max_digits=18, decimal_places=2)),
                ('credito', models.DecimalField(default=0.0, verbose_name=b'Credito', max_digits=18, decimal_places=2)),
                ('auxiliar', models.ForeignKey(verbose_name=b'Aux', blank=True, to='cuenta.Auxiliares', null=True)),
                ('cuenta', models.ForeignKey(verbose_name=b'Cuenta Contable', blank=True, to='cuenta.Cuentas', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DetalleCuentasRetiroAhorro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('debito', models.DecimalField(default=0.0, verbose_name=b'Debito', max_digits=18, decimal_places=2)),
                ('credito', models.DecimalField(default=0.0, verbose_name=b'Credito', max_digits=18, decimal_places=2)),
                ('auxiliar', models.ForeignKey(verbose_name=b'Aux', blank=True, to='cuenta.Auxiliares', null=True)),
                ('cuenta', models.ForeignKey(verbose_name=b'Cuenta Contable', blank=True, to='cuenta.Cuentas', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MaestraAhorro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField()),
                ('monto', models.DecimalField(verbose_name=b'Monto', max_digits=18, decimal_places=2)),
                ('interes', models.DecimalField(verbose_name=b'Interes', max_digits=18, decimal_places=2)),
                ('balance', models.DecimalField(verbose_name=b'Balance', max_digits=18, decimal_places=2)),
                ('estatus', models.BooleanField(default=False)),
                ('beneficiario', models.ForeignKey(blank=True, to='administracion.CoBeneficiario', null=True)),
                ('socio', models.ForeignKey(blank=True, to='administracion.Socio', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RetiroAhorro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipoRetiro', models.CharField(max_length=1, verbose_name=b'Tipo de Retiro', choices=[(b'A', b'Retiro Ahorro'), (b'J', b'Retiro por Ajuste'), (b'O', b'Otros')])),
                ('monto', models.DecimalField(default=0.0, verbose_name=b'Monto a Retirar', max_digits=18, decimal_places=2)),
                ('ahorro', models.ForeignKey(to='ahorro.AhorroSocio')),
                ('beneficiario', models.ForeignKey(blank=True, to='administracion.CoBeneficiario', null=True)),
                ('socio', models.ForeignKey(blank=True, to='administracion.Socio', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='detallecuentasretiroahorro',
            name='referencia',
            field=models.ForeignKey(to='ahorro.RetiroAhorro'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='detallecuentamaestraahorro',
            name='referencia',
            field=models.ForeignKey(to='ahorro.MaestraAhorro'),
            preserve_default=True,
        ),
    ]
