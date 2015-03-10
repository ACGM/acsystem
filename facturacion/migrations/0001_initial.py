# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administracion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detalle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('porcentajeDescuento', models.DecimalField(default=0, verbose_name=b'Porcentaje Descuento', max_digits=6, decimal_places=2, blank=True)),
                ('cantidad', models.DecimalField(max_digits=12, decimal_places=2)),
                ('precio', models.DecimalField(max_digits=12, decimal_places=2)),
                ('costo', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('almacen', models.ForeignKey(to='inventario.Almacen')),
            ],
            options={
                'ordering': ('-factura',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('posteo', models.CharField(default=b'N', max_length=1, choices=[(b'N', b'NO'), (b'S', b'SI')])),
                ('noFactura', models.PositiveIntegerField(unique=True, verbose_name=b'No. Factura')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('estatus', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Activa'), (b'I', b'Inactiva'), (b'N', b'Anulada')])),
                ('descrpAnulacion', models.CharField(max_length=150, null=True, blank=True)),
                ('ordenCompra', models.PositiveIntegerField(null=True, blank=True)),
                ('terminos', models.CharField(default=b'CO', max_length=2, choices=[(b'CO', b'Contado'), (b'CR', b'Credito')])),
                ('impresa', models.PositiveIntegerField(default=0)),
                ('datetimeServer', models.DateTimeField(auto_now_add=True)),
                ('localidad', models.ForeignKey(blank=True, to='administracion.Localidad', null=True)),
                ('socio', models.ForeignKey(to='administracion.Socio', null=True)),
                ('userLog', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-noFactura'],
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
        migrations.AlterUniqueTogether(
            name='detalle',
            unique_together=set([('factura', 'producto')]),
        ),
    ]
