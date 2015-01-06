# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0003_remove_detalle_pruebacampo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='detalle',
            options={'ordering': ('-factura',)},
        ),
        migrations.AlterModelOptions(
            name='factura',
            options={'ordering': ['-noFactura']},
        ),
    ]
