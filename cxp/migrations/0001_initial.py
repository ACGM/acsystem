# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0005_auto_20150211_2334'),
        ('cuenta', '__first__'),
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
                ('estatus', models.BooleanField(default=False)),
                ('detalleCuentas', models.ManyToManyField(related_name='diario_super_ref', verbose_name=b'Detalle Cuentas', to='cuenta.DiarioGeneral')),
                ('suplidor', models.ForeignKey(default=False, verbose_name=b'Suplidor', to='administracion.Suplidor')),
            ],
            options={
                'ordering': ['suplidor', 'fecha'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DetalleOrden',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('articulo', models.CharField(default=False, max_length=200, verbose_name=b'Articulo')),
                ('monto', models.DecimalField(verbose_name=b'Precio', max_digits=18, decimal_places=2)),
                ('orden', models.PositiveIntegerField(verbose_name=b'Orden Compra')),
            ],
            options={
                'ordering': ['articulo'],
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
                ('estatus', models.BooleanField(default=False)),
                ('detalleCuentas', models.ManyToManyField(related_name='diario_ref', verbose_name=b'Detalle Cuentas', to='cuenta.DiarioGeneral')),
                ('detalleOrden', models.ManyToManyField(related_name='detalle_ref', verbose_name=b'Detalle de Orden', to='cxp.DetalleOrden')),
                ('socio', models.ForeignKey(default=False, verbose_name=b'Socio', to='administracion.Socio')),
                ('suplidor', models.ForeignKey(default=False, verbose_name=b'Suplidor', to='administracion.Suplidor')),
            ],
            options={
                'ordering': ['suplidor', 'fecha'],
            },
            bases=(models.Model,),
        ),
    ]
