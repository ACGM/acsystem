# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='archivobancodetailn',
            name='prueba',
            field=models.CharField(default=b's', max_length=1),
            preserve_default=True,
        ),
    ]
