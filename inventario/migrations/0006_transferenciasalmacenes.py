# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administracion', '0022_auto_20150203_0153'),
        ('inventario', '0005_inventarioh_estatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransferenciasAlmacenes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.DecimalField(max_digits=12, decimal_places=2)),
                ('fechaTransf', models.DateField()),
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
    ]
