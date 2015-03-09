# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuenta', '__first__'),
        ('cxp', '0008_auto_20150305_0229'),
    ]

    operations = [
        migrations.CreateModel(
            name='CuentasGenericasOrdenes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('origen', models.CharField(max_length=1, choices=[(b'D', b'Debito'), (b'C', b'Credito')])),
                ('aux', models.ForeignKey(blank=True, to='cuenta.Auxiliares', null=True)),
                ('cuenta', models.ForeignKey(blank=True, to='cuenta.Cuentas', null=True)),
            ],
            options={
                'ordering': ['origen'],
            },
            bases=(models.Model,),
        ),
    ]
