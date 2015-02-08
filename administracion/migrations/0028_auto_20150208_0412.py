# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0027_auto_20150206_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivobancodetailn',
            name='descrpEstadoDestino',
            field=models.CharField(default=b'', max_length=40, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='archivobancodetailn',
            name='emailBenef',
            field=models.CharField(default=b'', max_length=40, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='archivobancodetailn',
            name='faxTelefonoBenef',
            field=models.CharField(default=b'', max_length=12, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='archivobancodetailn',
            name='fechaVencimiento',
            field=models.CharField(default=b'', max_length=4, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='archivobancodetailn',
            name='filler2',
            field=models.CharField(default=b'', max_length=52, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='archivobancodetailn',
            name='lineaFormateadaN',
            field=models.CharField(max_length=320, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='archivobancodetailn',
            name='numeroAut',
            field=models.CharField(default=b'', max_length=15, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='archivobancodetailn',
            name='numeroReferencia',
            field=models.CharField(default=b'', max_length=12, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='archivobancodetailn',
            name='tipoRegistro',
            field=models.CharField(default=b'N', max_length=1, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='archivobancoheader',
            name='estatus',
            field=models.CharField(max_length=1, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='archivobancoheader',
            name='filler',
            field=models.CharField(max_length=107, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='archivobancoheader',
            name='lineaFormateadaH',
            field=models.CharField(max_length=292, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='archivobancoheader',
            name='numeroAfiliacion',
            field=models.CharField(max_length=15, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaInicioAhorro',
            field=models.DateField(default=datetime.datetime(2015, 2, 8, 4, 12, 26, 526401), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaModificacion',
            field=models.DateField(default=datetime.datetime(2015, 2, 8, 4, 12, 26, 526422), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='empresa',
            name='nombre',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
    ]
