# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ahorro', '0003_retiroahorro_estatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='retiroahorro',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2015, 3, 16, 2, 26, 20, 983000, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
