# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cxp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cxpsupercoopdetallecuentas',
            options={'ordering': ['cuenta', 'auxiliar']},
        ),
        migrations.AlterModelOptions(
            name='detallecuentasorden',
            options={'ordering': ['cuenta', 'auxiliar']},
        ),
        migrations.AlterModelOptions(
            name='detalleorden',
            options={'ordering': ['articulo']},
        ),
        migrations.RemoveField(
            model_name='cxpsupercoopdetallecuentas',
            name='cxcSupercoop',
        ),
        migrations.RemoveField(
            model_name='detallecuentasorden',
            name='orden',
        ),
        migrations.RemoveField(
            model_name='detalleorden',
            name='orden',
        ),
        migrations.AddField(
            model_name='cxpsupercoop',
            name='detalleCuentas',
            field=models.ForeignKey(default=1, verbose_name=b'Cuentas', to='cxp.CxpSuperCoopDetalleCuentas'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ordencompra',
            name='detalleCuentas',
            field=models.ForeignKey(default=2, verbose_name=b'Detalle Cuentas', to='cxp.DetalleCuentasOrden'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ordencompra',
            name='detalleOrden',
            field=models.ForeignKey(default=2, verbose_name=b'Detalle de Orden', to='cxp.DetalleOrden'),
            preserve_default=False,
        ),
    ]
