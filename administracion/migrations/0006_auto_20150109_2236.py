# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0005_auto_20150108_0410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='costo',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='producto',
            name='descripcion',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio',
            field=models.DecimalField(max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socio',
            name='celular',
            field=models.CharField(max_length=40, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socio',
            name='ciudad',
            field=models.CharField(max_length=40, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socio',
            name='nombreCompleto',
            field=models.CharField(verbose_name=b'Nombre Completo', max_length=80, editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socio',
            name='sector',
            field=models.CharField(max_length=40, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socio',
            name='telefono',
            field=models.CharField(max_length=40, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='suplidor',
            name='ciudad',
            field=models.CharField(max_length=40, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='suplidor',
            name='contacto',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='suplidor',
            name='nombre',
            field=models.CharField(max_length=60),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='suplidor',
            name='sector',
            field=models.CharField(max_length=40, blank=True),
            preserve_default=True,
        ),
    ]
