# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nominacoop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nominacooph',
            name='posteada',
            field=models.CharField(default=b'N', max_length=1),
            preserve_default=True,
        ),
    ]
