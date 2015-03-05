# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cxp', '0005_ordencompra_estatus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detalleorden',
            name='orden',
        ),
    ]
