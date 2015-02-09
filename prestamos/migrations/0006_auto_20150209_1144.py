# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prestamos', '0005_auto_20150208_1644'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitudordendespachoh',
            name='unificarPrestamos',
        ),
        migrations.AddField(
            model_name='solicitudordendespachoh',
            name='fechaVencimiento',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='solicitudordendespachoh',
            name='prestamo',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
