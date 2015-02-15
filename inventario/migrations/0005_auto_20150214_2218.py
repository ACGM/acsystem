# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0005_auto_20150211_2334'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventario', '0004_ajusteinventario'),
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
                ('datetimeServer', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('fecha',),
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='ajusteinventario',
            name='almacen',
        ),
        migrations.RemoveField(
            model_name='ajusteinventario',
            name='producto',
        ),
        migrations.DeleteModel(
            name='AjusteInventario',
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
