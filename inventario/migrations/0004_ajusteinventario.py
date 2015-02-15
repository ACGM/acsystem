# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0005_auto_20150211_2334'),
        ('inventario', '0003_remove_inventarioh_prueba'),
    ]

    operations = [
        migrations.CreateModel(
            name='AjusteInventario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidadFisico', models.DecimalField(max_digits=12, decimal_places=2, blank=True)),
                ('cantidadTeorico', models.DecimalField(max_digits=12, decimal_places=2, blank=True)),
                ('notaAjuste', models.CharField(max_length=200, null=True, blank=True)),
                ('almacen', models.ForeignKey(to='inventario.Almacen')),
                ('producto', models.ForeignKey(to='administracion.Producto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
