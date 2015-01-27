# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('prestamos', '0007_auto_20150127_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudprestamo',
            name='autorizadoPor',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
