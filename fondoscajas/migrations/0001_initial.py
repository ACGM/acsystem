# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administracion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConceptoDesembolso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=255)),
                ('cuentaCredito', models.ForeignKey(related_name='+', to='administracion.CuentaContable')),
                ('cuentaDebito', models.ForeignKey(related_name='+', to='administracion.CuentaContable')),
            ],
            options={
                'ordering': ['descripcion'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DesembolsoD',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('monto', models.DecimalField(max_digits=12, decimal_places=2)),
                ('concepto', models.ForeignKey(to='fondoscajas.ConceptoDesembolso')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DesembolsoH',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('beneficiario', models.TextField()),
                ('monto', models.DecimalField(max_digits=12, decimal_places=2)),
                ('fecha', models.DateField(auto_now=True)),
                ('estatus', models.CharField(default=b'A', max_length=1)),
                ('impreso', models.PositiveIntegerField(default=0)),
                ('datetimeServer', models.DateTimeField(auto_now_add=True)),
                ('userLog', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fondo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=150)),
                ('estatus', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Activo'), (b'I', b'Inhactivo')])),
            ],
            options={
                'ordering': ['descripcion'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='desembolsod',
            name='desembolso',
            field=models.ForeignKey(to='fondoscajas.DesembolsoH'),
            preserve_default=True,
        ),
    ]
