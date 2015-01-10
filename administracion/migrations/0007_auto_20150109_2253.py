# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0006_auto_20150109_2236'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='producto',
            unique_together=set([('codigo',)]),
        ),
    ]
