# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


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
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AjusteInventarioH',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('notaAjuste', models.CharField(max_length=200, null=True, blank=True)),
                ('estatus', models.CharField(default=b'E', max_length=1)),
                ('datetimeServer', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('id',),
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
                ('descripcionSalida', models.CharField(max_length=255, null=True, verbose_name=b'Descripci\xc3\xb3n de Salida', blank=True)),
                ('fechaSalida', models.DateTimeField(null=True, verbose_name=b'Fecha de Salida', blank=True)),
                ('numeroSalida', models.PositiveIntegerField(default=0, null=True, blank=True)),
                ('posteo', models.CharField(default=b'N', max_length=1, choices=[(b'N', b'NO'), (b'S', b'SI')])),
                ('condicion', models.CharField(default=b'CO', max_length=2, choices=[(b'CO', b'Contado'), (b'CR', b'Credito')])),
                ('datetimeServer', models.DateTimeField(auto_now_add=True)),
                ('suplidor', models.ForeignKey(to='administracion.Suplidor')),
                ('userLog', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('usuarioSalida', models.ForeignKey(related_name='+', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': 'Inventario Cabecera',
                'verbose_name_plural': 'Inventario Cabecera',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Movimiento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.DecimalField(max_digits=12, decimal_places=2)),
                ('fecha_movimiento', models.DateField(auto_now_add=True)),
                ('tipo_mov', models.CharField(default=b'E', max_length=1, verbose_name=b'Tipo de Movimiento', choices=[(b'E', b'Entrada'), (b'S', b'Salida')])),
                ('datetime_server', models.DateTimeField(auto_now_add=True)),
                ('almacen', models.ForeignKey(to='inventario.Almacen')),
                ('producto', models.ForeignKey(to='administracion.Producto')),
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
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='inventariod',
            name='inventario',
            field=models.ForeignKey(to='inventario.InventarioH'),
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
