# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administracion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AjusteInventarioD',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidadFisico', models.DecimalField(max_digits=12, decimal_places=2, blank=True)),
                ('cantidadTeorico', models.DecimalField(max_digits=12, decimal_places=2, blank=True)),
            ],
            options={
                'verbose_name': 'Ajuste Inventario Detalle',
                'verbose_name_plural': 'Ajuste Inventario Detalle',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AjusteInventarioH',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('notaAjuste', models.CharField(max_length=200, null=True, blank=True)),
                ('estatus', models.CharField(default=b'N', max_length=1)),
                ('datetimeServer', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': 'Ajuste Inventario Cabecera',
                'verbose_name_plural': 'Ajuste Inventario Cabecera',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Almacen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['descripcion'],
                'verbose_name_plural': 'Almacenes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Existencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.DecimalField(max_digits=12, decimal_places=2)),
                ('cantidadAnterior', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('fecha', models.DateField(auto_now=True)),
                ('almacen', models.ForeignKey(to='inventario.Almacen')),
                ('producto', models.ForeignKey(to='administracion.Producto')),
            ],
            options={
                'ordering': ['producto'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InventarioD',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidadTeorico', models.DecimalField(max_digits=12, decimal_places=2)),
                ('cantidadFisico', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('costo', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('tipoAccion', models.CharField(default=b'E', max_length=1, verbose_name=b'Tipo de Accion', choices=[(b'E', b'Entrada'), (b'S', b'Salida')])),
                ('almacen', models.ForeignKey(to='inventario.Almacen')),
            ],
            options={
                'verbose_name': 'Inventario Detalle',
                'verbose_name_plural': 'Inventario Detalle',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InventarioH',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(default=datetime.datetime.now)),
                ('orden', models.CharField(max_length=30, null=True, blank=True)),
                ('factura', models.CharField(max_length=12, null=True, blank=True)),
                ('diasPlazo', models.CharField(max_length=3, null=True, verbose_name=b'Dias de Plazo', blank=True)),
                ('nota', models.TextField(null=True, blank=True)),
                ('ncf', models.CharField(max_length=25, null=True, verbose_name=b'NCF', blank=True)),
                ('posteo', models.CharField(default=b'N', max_length=1, choices=[(b'N', b'NO'), (b'S', b'SI')])),
                ('condicion', models.CharField(default=b'CO', max_length=2, choices=[(b'CO', b'Contado'), (b'CR', b'Credito')])),
                ('cxp', models.CharField(default=b'E', max_length=1, choices=[(b'E', b'EN PROCESO'), (b'P', b'PROCESADA')])),
                ('borrado', models.BooleanField(default=False)),
                ('borradoFecha', models.DateTimeField(null=True)),
                ('datetimeServer', models.DateTimeField(auto_now_add=True)),
                ('borradoPor', models.ForeignKey(related_name='+', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('suplidor', models.ForeignKey(to='administracion.Suplidor')),
                ('userLog', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': 'Inventario Cabecera',
                'verbose_name_plural': 'Inventario Cabecera',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InventarioHSalidas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(default=datetime.datetime.now)),
                ('descripcionSalida', models.CharField(max_length=255, null=True, verbose_name=b'Descripci\xc3\xb3n de Salida', blank=True)),
                ('posteo', models.CharField(default=b'N', max_length=1, choices=[(b'N', b'NO'), (b'S', b'SI')])),
                ('borrado', models.BooleanField(default=False)),
                ('borradoFecha', models.DateTimeField(null=True)),
                ('datetimeServer', models.DateTimeField(auto_now_add=True)),
                ('borradoPor', models.ForeignKey(related_name='+', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('usuarioSalida', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': 'Inventario Cabecera SALIDAS',
                'verbose_name_plural': 'Inventario Cabecera SALIDAS',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Movimiento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.DecimalField(max_digits=12, decimal_places=2)),
                ('precio', models.DecimalField(null=True, max_digits=12, decimal_places=2)),
                ('costo', models.DecimalField(null=True, max_digits=12, decimal_places=2)),
                ('fechaMovimiento', models.DateField(auto_now_add=True)),
                ('documento', models.CharField(max_length=4, choices=[(b'EINV', b'Entrada Inventario'), (b'SINV', b'Salida Inventario'), (b'AINV', b'Ajuste Inventario'), (b'FACT', b'Facturacion')])),
                ('documentoNo', models.PositiveIntegerField()),
                ('tipo_mov', models.CharField(default=b'E', max_length=1, verbose_name=b'Tipo de Movimiento', choices=[(b'E', b'Entrada'), (b'S', b'Salida')])),
                ('datetime_server', models.DateTimeField(auto_now_add=True)),
                ('almacen', models.ForeignKey(to='inventario.Almacen')),
                ('producto', models.ForeignKey(to='administracion.Producto')),
                ('userLog', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['producto'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransferenciasAlmacenes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.DecimalField(max_digits=12, decimal_places=2)),
                ('fechaTransf', models.DateField(auto_now_add=True)),
                ('desdeAlmacen', models.ForeignKey(related_name='+', to='inventario.Almacen')),
                ('hastaAlmacen', models.ForeignKey(related_name='+', to='inventario.Almacen')),
                ('producto', models.ForeignKey(to='administracion.Producto')),
                ('userLog', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('fechaTransf',),
                'verbose_name': 'Transferencia entre Almacenes',
                'verbose_name_plural': 'Transferencias entre Almacenes',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='inventariod',
            name='inventario',
            field=models.ForeignKey(to='inventario.InventarioH', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inventariod',
            name='inventarioSalida',
            field=models.ForeignKey(to='inventario.InventarioHSalidas', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inventariod',
            name='producto',
            field=models.ForeignKey(to='administracion.Producto'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='existencia',
            unique_together=set([('producto', 'almacen')]),
        ),
        migrations.AddField(
            model_name='ajusteinventariod',
            name='ajusteInvH',
            field=models.ForeignKey(to='inventario.AjusteInventarioH'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ajusteinventariod',
            name='almacen',
            field=models.ForeignKey(to='inventario.Almacen'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ajusteinventariod',
            name='producto',
            field=models.ForeignKey(to='administracion.Producto'),
            preserve_default=True,
        ),
    ]
