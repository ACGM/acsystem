# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prestamos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudordendespachoh',
            name='montoSolicitado',
            field=models.DecimalField(max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='solicitudordendespachoh',
            name='netoDesembolsar',
            field=models.DecimalField(max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='solicitudordendespachoh',
            name='salarioSocio',
            field=models.DecimalField(max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='solicitudordendespachoh',
            name='valorCuotasCapital',
            field=models.DecimalField(max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='solicitudordendespachoh',
            name='valorGarantizdo',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='solicitudprestamo',
            name='montoSolicitado',
            field=models.DecimalField(max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='solicitudprestamo',
            name='netoDesembolsar',
            field=models.DecimalField(max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='solicitudprestamo',
            name='noSolicitud',
            field=models.PositiveIntegerField(unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='solicitudprestamo',
            name='observacion',
            field=models.TextField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='solicitudprestamo',
            name='salarioSocio',
            field=models.DecimalField(max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='solicitudprestamo',
            name='valorCuotasCapital',
            field=models.DecimalField(max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='solicitudprestamo',
            name='valorGarantizado',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
