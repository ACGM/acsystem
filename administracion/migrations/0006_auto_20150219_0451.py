# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0005_auto_20150211_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='codigo',
            field=models.CharField(unique=True, max_length=10, editable=False),
            preserve_default=True,
        ),
    ]
