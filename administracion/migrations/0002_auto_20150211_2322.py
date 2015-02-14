# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoriaprestamo',
            name='interesAnualDirectivo',
        ),
        migrations.RemoveField(
            model_name='categoriaprestamo',
            name='interesAnualEmpleado',
        ),
        migrations.AlterField(
            model_name='categoriaprestamo',
            name='interesAnualSocio',
            field=models.DecimalField(null=True, verbose_name=b'Intereses Anual Socio %', max_digits=6, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='suplidor',
            name='cedulaRNC',
            field=models.CharField(unique=True, max_length=25, verbose_name=b'Cedula o RNC'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='suplidor',
            name='intereses',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, blank=True, null=True, verbose_name=b'Intereses %'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='suplidor',
            name='tipoIdentificacion',
            field=models.CharField(default=b'C', max_length=1, verbose_name=b'Tipo de Identificacion', choices=[(b'C', b'Cedula'), (b'R', b'RNC')]),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='documentocuentas',
            unique_together=set([('documento', 'cuenta', 'accion')]),
        ),
    ]
