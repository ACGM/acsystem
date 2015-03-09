# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cxp', '0009_cuentasgenericasordenes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuentasgenericasordenes',
            name='aux',
        ),
        migrations.RemoveField(
            model_name='cuentasgenericasordenes',
            name='cuenta',
        ),
        migrations.DeleteModel(
            name='CuentasGenericasOrdenes',
        ),
    ]
