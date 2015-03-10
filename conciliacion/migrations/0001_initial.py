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
            name='ConcCheques',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chequeNo', models.PositiveIntegerField(verbose_name=b'# Cheque')),
                ('fecha', models.DateTimeField()),
                ('estatus', models.CharField(max_length=1, verbose_name=b'Estatus', choices=[(b'p', b'Posteado'), (b'R', b'Registrado'), (b'C', b'Cancelado'), (b'D', b'Devueltos')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NotaDCConciliacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('concepto', models.CharField(max_length=150, verbose_name=b'Concepto')),
                ('fecha', models.DateTimeField()),
                ('tipo', models.CharField(max_length=1, verbose_name=b'Tipo Nota', choices=[(b'D', b'Debito'), (b'C', b'Credito')])),
                ('monto', models.DecimalField(max_digits=18, decimal_places=2)),
                ('estatus', models.CharField(default=b'R', max_length=1, choices=[(b'P', b'Posteada'), (b'R', b'Registrado'), (b'N', b'Nula')])),
                ('cuentas', models.ManyToManyField(related_name='NConci_rel', verbose_name=b'Cuentas', to='cuenta.DiarioGeneral')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SolicitudCheque',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField()),
                ('concepto', models.CharField(max_length=150)),
                ('monto', models.DecimalField(verbose_name=b'Monto', max_digits=18, decimal_places=2)),
                ('beneficiario', models.ForeignKey(to='administracion.CoBeneficiario')),
                ('cuentas', models.ManyToManyField(related_name='Solicitud_rel', verbose_name=b'Cuentas', to='cuenta.DiarioGeneral')),
                ('socio', models.ForeignKey(to='administracion.Socio')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='conccheques',
            name='solicitud',
            field=models.ForeignKey(to='conciliacion.SolicitudCheque'),
            preserve_default=True,
        ),
    ]
