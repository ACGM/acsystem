# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administracion', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Almacen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['descripcion'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Existencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.IntegerField()),
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
                ('cantidadTeorico', models.PositiveIntegerField()),
                ('cantidadFisico', models.PositiveIntegerField()),
                ('costo', models.DecimalField(max_digits=18, decimal_places=2, blank=True)),
                ('tipoAccion', models.CharField(default=b'E', max_length=1, verbose_name=b'Tipo de Accion', choices=[(b'E', b'Entrada'), (b'S', b'Salida')])),
                ('almacen', models.ForeignKey(to='inventario.Almacen')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InventarioH',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(default=datetime.datetime.now)),
                ('orden', models.CharField(max_length=30)),
                ('factura', models.CharField(max_length=30)),
                ('diasPlazo', models.CharField(default=b'30', max_length=3, choices=[(b'30', b'30'), (b'60', b'60'), (b'120', b'120')])),
                ('nota', models.TextField(blank=True)),
                ('ncf', models.CharField(max_length=25, blank=True)),
                ('descripcionSalida', models.CharField(max_length=255, verbose_name=b'Descripci\xc3\xb3n de Salida', blank=True)),
                ('datetimeServer', models.DateTimeField(auto_now_add=True)),
                ('almacen', models.ForeignKey(to='inventario.Almacen')),
                ('userLog', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Movimiento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.IntegerField()),
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
    ]
