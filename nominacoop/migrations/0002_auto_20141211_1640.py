# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nominacoop', '0001_initial'),
        ('prestamos', '0001_initial'),
        ('administracion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuotasprestamosempresa',
            name='cuota',
            field=models.ForeignKey(to='prestamos.CuotasPrestamo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cuotasprestamosempresa',
            name='noPrestamo',
            field=models.ForeignKey(to='prestamos.MaestraPrestamo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cuotasprestamosempresa',
            name='socio',
            field=models.ForeignKey(to='administracion.Socio'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cuotasahorrosempresa',
            name='cuota',
            field=models.ForeignKey(to='prestamos.CuotasPrestamo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cuotasahorrosempresa',
            name='noPrestamo',
            field=models.ForeignKey(to='prestamos.MaestraPrestamo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cuotasahorrosempresa',
            name='socio',
            field=models.ForeignKey(to='administracion.Socio'),
            preserve_default=True,
        ),
    ]
