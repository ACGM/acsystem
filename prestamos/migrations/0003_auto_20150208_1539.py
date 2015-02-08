# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prestamos', '0002_solicitudprestamo_aprobadorechazadopor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maestraprestamo',
            name='balance',
            field=models.DecimalField(default=0, max_digits=12, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='maestraprestamo',
            name='distrito',
            field=models.ForeignKey(blank=True, to='administracion.Distrito', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='maestraprestamo',
            name='factura',
            field=models.ForeignKey(blank=True, to='facturacion.Factura', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='maestraprestamo',
            name='fechaDesembolso',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='maestraprestamo',
            name='fechaEntrega',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
