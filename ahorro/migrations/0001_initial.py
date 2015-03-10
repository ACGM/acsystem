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
            name='AhorroSocio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('balance', models.DecimalField(verbose_name=b'Balance Socio', max_digits=18, decimal_places=2)),
                ('disponible', models.DecimalField(verbose_name=b'Disponible', max_digits=18, decimal_places=2)),
                ('socio', models.ForeignKey(to='administracion.Socio', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InteresesAhorro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=100, verbose_name=b'Descripcion')),
                ('porcentaje', models.DecimalField(max_digits=2, decimal_places=2)),
            ],
            options={
                'ordering': ['descripcion'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MaestraAhorro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('monto', models.DecimalField(verbose_name=b'Monto', max_digits=18, decimal_places=2)),
                ('balance', models.DecimalField(verbose_name=b'Balance', max_digits=18, decimal_places=2)),
                ('estatus', models.BooleanField(default=False)),
                ('ahorro', models.ForeignKey(to='ahorro.AhorroSocio')),
                ('cuentas', models.ManyToManyField(related_name='ahorro_rel', verbose_name=b'Cuentas', to='cuenta.DiarioGeneral')),
                ('interes', models.ForeignKey(to='ahorro.InteresesAhorro')),
            ],
            options={
                'ordering': ['fecha'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RetiroAhorro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipoRetiro', models.CharField(max_length=1, verbose_name=b'Tipo de Retiro', choices=[(b'A', b'Retiro Ahorro'), (b'J', b'Retiro por Ajuste'), (b'O', b'Otros')])),
                ('monto', models.DecimalField(default=0.0, verbose_name=b'Monto a Retirar', max_digits=18, decimal_places=2)),
                ('ahorro', models.ForeignKey(to='ahorro.AhorroSocio')),
                ('socio', models.ForeignKey(to='administracion.Socio')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='maestraahorro',
            name='retiro',
            field=models.ForeignKey(blank=True, to='ahorro.RetiroAhorro', null=True),
            preserve_default=True,
        ),
    ]
