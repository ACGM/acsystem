# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ahorro', '0001_initial'),
        ('prestamos', '0001_initial'),
        ('administracion', '0001_initial'),
        ('cuenta', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleCuentasRecibo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('debito', models.DecimalField(default=0.0, verbose_name=b'Debito', max_digits=18, decimal_places=2)),
                ('credito', models.DecimalField(default=0.0, verbose_name=b'Credito', max_digits=18, decimal_places=2)),
                ('auxiliar', models.ForeignKey(verbose_name=b'Aux', blank=True, to='cuenta.Auxiliares', null=True)),
                ('cuenta', models.ForeignKey(verbose_name=b'Cuenta Contable', blank=True, to='cuenta.Cuentas', null=True)),
                ('referencia', models.ForeignKey(to='prestamos.MaestraPrestamo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DetalleRecibo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('montoCuota', models.DecimalField(verbose_name=b'Monto Cuota', max_digits=18, decimal_places=2)),
                ('montoDistribuir', models.DecimalField(verbose_name=b'Por Distribuir', max_digits=18, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RecibosIngreso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('montoPrestamo', models.DecimalField(default=0.0, verbose_name=b'Rebajar a PRestamo', max_digits=18, decimal_places=2)),
                ('montoAhorro', models.DecimalField(default=0.0, verbose_name=b'Ingreso a Ahorro', max_digits=18, decimal_places=2)),
                ('estatus', models.BooleanField(default=False)),
                ('ahorro', models.ForeignKey(blank=True, to='ahorro.AhorroSocio', null=True)),
                ('prestamo', models.ForeignKey(blank=True, to='prestamos.MaestraPrestamo', null=True)),
                ('socioIngreso', models.ForeignKey(to='administracion.Socio')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='detallerecibo',
            name='recibo',
            field=models.ForeignKey(to='reciboingreso.RecibosIngreso'),
            preserve_default=True,
        ),
    ]
