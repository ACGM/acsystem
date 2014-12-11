# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administracion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detalle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('porcentajeDescuento', models.DecimalField(default=0, max_digits=6, decimal_places=2, blank=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('precio', models.PositiveIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('noFactura', models.IntegerField(unique=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('estatus', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Activa'), (b'I', b'Inactiva'), (b'N', b'Anulada')])),
                ('descrpAnulacion', models.CharField(max_length=255, blank=True)),
                ('ordenCompra', models.CharField(max_length=20, blank=True)),
                ('terminos', models.CharField(default=b'CO', max_length=2, choices=[(b'CO', b'Contado'), (b'CR', b'Credito')])),
                ('impresa', models.IntegerField(default=0)),
                ('datetimeServer', models.DateTimeField(auto_now_add=True)),
                ('socio', models.ForeignKey(to='administracion.Socio')),
                ('userLog', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-noFactura'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrdenDespachoSuperCoop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('noSolicitud', models.IntegerField()),
                ('pagarPor', models.CharField(default=b'EM', max_length=2, choices=[(b'EM', b'Empresa'), (b'CA', b'Cajero')])),
                ('formaPago', models.CharField(default=b'Q', max_length=1, choices=[(b'Q', b'Quincenal'), (b'M', b'Mensual')])),
                ('tasaInteresAnual', models.DecimalField(default=0, max_digits=6, decimal_places=2)),
                ('tasaInteresMensual', models.DecimalField(default=0, max_digits=6, decimal_places=2)),
                ('quincena', models.IntegerField(default=b'1', blank=True, choices=[(b'1', b'1ra Quincena'), (b'2', b'2da Quincena')])),
                ('cuotas', models.IntegerField(default=2)),
                ('valorCuotas', models.DecimalField(max_digits=12, decimal_places=2)),
                ('estatus', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Activa'), (b'I', b'Inactiva'), (b'N', b'Anulada')])),
                ('datetimeServer', models.DateTimeField(auto_now_add=True)),
                ('categoria', models.ForeignKey(to='administracion.CategoriaPrestamo')),
                ('oficial', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['noSolicitud'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='detalle',
            name='factura',
            field=models.ForeignKey(to='facturacion.Factura'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='detalle',
            name='producto',
            field=models.ForeignKey(to='administracion.Producto'),
            preserve_default=True,
        ),
    ]
