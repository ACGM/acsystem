# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prestamos', '0003_solicitudordendespachoh_localidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maestraprestamo',
            name='chequeNo',
            field=models.ForeignKey(blank=True, to='prestamos.Cheque', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='solicitudordendespachoh',
            name='localidad',
            field=models.ForeignKey(to='administracion.Localidad'),
            preserve_default=True,
        ),
    ]
