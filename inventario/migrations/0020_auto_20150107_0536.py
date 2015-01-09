# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0019_auto_20150107_0510'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='existencia',
            unique_together=set([('producto', 'almacen')]),
        ),
    ]
