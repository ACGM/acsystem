# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuenta', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='MayorGeneral',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('agno', models.PositiveIntegerField(default=False, max_length=4, verbose_name=b'Agno')),
                ('mes', models.PositiveIntegerField(default=False, max_length=12, verbose_name=b'Mes')),
                ('dia', models.PositiveIntegerField(default=False, max_length=31, verbose_name=b'Dia')),
                ('debito', models.DecimalField(default=False, verbose_name=b'Debito', max_digits=18, decimal_places=2)),
                ('credito', models.DecimalField(default=False, verbose_name=b'Credito', max_digits=18, decimal_places=2)),
                ('balance', models.DecimalField(default=False, verbose_name=b'Balance', max_digits=18, decimal_places=2)),
                ('cuenta', models.ForeignKey(verbose_name=b'Cuenta Contable', to='cuenta.Cuentas')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
