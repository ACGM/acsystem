# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0008_remove_representante_prueba'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='correoHeader',
            field=models.CharField(max_length=40, null=True, blank=True),
            preserve_default=True,
        ),
    ]
