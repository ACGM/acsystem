# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ahorro', '0002_auto_20150310_0243'),
    ]

    operations = [
        migrations.AddField(
            model_name='retiroahorro',
            name='estatus',
            field=models.CharField(default=b'A', max_length=1, verbose_name=b'Estatus', choices=[(b'A', b'Activas'), (b'I', b'Inactivas'), (b'P', b'Posteada')]),
            preserve_default=True,
        ),
    ]
