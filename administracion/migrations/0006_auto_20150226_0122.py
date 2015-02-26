# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0005_remove_banco_prueba'),
    ]

    operations = [
        migrations.AddField(
            model_name='banco',
            name='codigoOperacion',
            field=models.CharField(default=b'22', max_length=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='banco',
            name='digitoVerificador',
            field=models.CharField(default=b'8', max_length=1),
            preserve_default=True,
        ),
    ]
