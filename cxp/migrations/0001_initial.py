# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuenta', '0002_auto_20141212_0235'),
        ('administracion', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CxpSuperCoop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('factura', models.CharField(default=False, max_length=10, verbose_name=b'# Factura')),
                ('fecha', models.DateField(verbose_name=b'Fecha')),
                ('concepto', models.CharField(default=False, max_length=255, verbose_name=b'Concepto')),
                ('monto', models.DecimalField(default=False, verbose_name=b'Monto', max_digits=18, decimal_places=2)),
                ('descuento', models.DecimalField(default=False, verbose_name=b'Desc', max_digits=18, decimal_places=2)),
                ('suplidor', models.ForeignKey(default=False, verbose_name=b'Suplidor', to='administracion.Suplidor')),
            ],
            options={
                'ordering': ['suplidor', 'fecha'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CxpSuperCoopDetalleCuentas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('debito', models.DecimalField(default=False, verbose_name=b'Debito', max_digits=18, decimal_places=2)),
                ('credito', models.DecimalField(default=False, verbose_name=b'Credito', max_digits=18, decimal_places=2)),
                ('auxiliar', models.ForeignKey(verbose_name=b'Cuenta', blank=True, to='cuenta.Auxiliares', null=True)),
                ('cuenta', models.ForeignKey(verbose_name=b'Cuenta', blank=True, to='cuenta.Cuentas', null=True)),
                ('cxcSupercoop', models.ForeignKey(default=False, verbose_name=b'Registro', to='cxp.CxpSuperCoop')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DetalleCuentasOrden',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('debito', models.DecimalField(default=False, verbose_name=b'Debito', max_digits=18, decimal_places=2)),
                ('credito', models.DecimalField(default=False, verbose_name=b'Credito', max_digits=18, decimal_places=2)),
                ('auxiliar', models.ForeignKey(verbose_name=b'Cuenta', blank=True, to='cuenta.Auxiliares', null=True)),
                ('cuenta', models.ForeignKey(verbose_name=b'Cuenta', blank=True, to='cuenta.Cuentas', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DetalleOrden',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('articulo', models.CharField(default=False, max_length=200, verbose_name=b'Articulo')),
                ('monto', models.DecimalField(verbose_name=b'Precio', max_digits=18, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrdenCompra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('orden', models.PositiveIntegerField(verbose_name=b'# Orden')),
                ('fecha', models.DateField(verbose_name=b'Fecha')),
                ('monto', models.DecimalField(verbose_name=b'Monto', max_digits=18, decimal_places=2)),
                ('cuotas', models.PositiveIntegerField(verbose_name=b'Cuotas')),
                ('montocuotas', models.DecimalField(max_digits=18, decimal_places=2)),
                ('socio', models.ForeignKey(default=False, verbose_name=b'Socio', to='administracion.Socio')),
                ('suplidor', models.ForeignKey(default=False, verbose_name=b'Suplidor', to='administracion.Suplidor')),
            ],
            options={
                'ordering': ['suplidor', 'fecha'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='detalleorden',
            name='orden',
            field=models.ForeignKey(default=False, verbose_name=b'Orden', to='cxp.OrdenCompra'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='detallecuentasorden',
            name='orden',
            field=models.ForeignKey(default=False, verbose_name=b'Orden', to='cxp.OrdenCompra'),
            preserve_default=True,
        ),
    ]
