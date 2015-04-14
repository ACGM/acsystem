# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nominacoop', '0003_auto_20150325_0039'),
    ]

    operations = [
        migrations.AddField(
            model_name='nominaprestamosahorros',
            name='infoTipo',
            field=models.CharField(max_length=4, null=True, blank=True),
            preserve_default=True,
        ),
    ]
