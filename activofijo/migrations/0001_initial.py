# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuenta', '__first__'),
        ('administracion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(default=None, max_length=100, verbose_name=b'Descripcion')),
                ('fechaAdd', models.DateTimeField(verbose_name=b'Fecha Adquisicion')),
                ('fechaDep', models.DateTimeField(verbose_name=b'Fecha Depresiacion')),
                ('agnosVu', models.PositiveIntegerField(verbose_name=b'Agnos vida Util')),
                ('costo', models.DecimalField(verbose_name=b'Costo de adquisicion', max_digits=18, decimal_places=2)),
                ('porcentaje', models.DecimalField(verbose_name=b'%. Dep Anual', max_digits=3, decimal_places=2)),
                ('factura', models.PositiveIntegerField(verbose_name=b'Factura')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CategoriaActivo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(default=None, unique=True, max_length=100, verbose_name=b'Categoria de Activo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Depresiacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dMensual', models.DecimalField(verbose_name=b'Depresiacion Mensual', max_digits=18, decimal_places=2)),
                ('dAcumulada', models.DecimalField(verbose_name=b'Depresiacion Acumulada', max_digits=18, decimal_places=2)),
                ('dAgno', models.DecimalField(verbose_name=b'Depresiacion en el Agno', max_digits=18, decimal_places=2)),
                ('vLibro', models.DecimalField(verbose_name=b'Valor en Libro', max_digits=18, decimal_places=2)),
                ('cuentas', models.ManyToManyField(related_name='depre_rel', verbose_name=b'Cuentas', to='cuenta.DiarioGeneral')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='activos',
            name='categoria',
            field=models.ForeignKey(to='activofijo.CategoriaActivo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activos',
            name='cuentas',
            field=models.ManyToManyField(related_name='ActivoCuentas_rel', verbose_name=b'Cuentas', to='cuenta.DiarioGeneral'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activos',
            name='depresiacion',
            field=models.ManyToManyField(related_name='ActivoDep_rel', verbose_name=b'Depresiaciones', to='activofijo.Depresiacion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activos',
            name='localidad',
            field=models.ForeignKey(verbose_name=b'Localidad', to='administracion.Localidad'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activos',
            name='suplidor',
            field=models.ForeignKey(verbose_name=b'Suplidor', to='administracion.Suplidor'),
            preserve_default=True,
        ),
    ]
