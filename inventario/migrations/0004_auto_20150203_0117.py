# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventario', '0003_auto_20150130_0449'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventarioh',
            name='fechaSalida',
            field=models.DateField(null=True, verbose_name=b'Fecha de Salida', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inventarioh',
            name='usuarioSalida',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
