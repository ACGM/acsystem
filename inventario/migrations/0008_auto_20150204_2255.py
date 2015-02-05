# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0007_remove_inventarioh_estatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventarioh',
            name='descripcionSalida',
            field=models.CharField(verbose_name=b'Descripci\xc3\xb3n de Salida', max_length=255, null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='inventarioh',
            name='fechaSalida',
            field=models.DateTimeField(verbose_name=b'Fecha de Salida', null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='inventarioh',
            name='usuarioSalida',
            field=models.ForeignKey(related_name='+', editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
