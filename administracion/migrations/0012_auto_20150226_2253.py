# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0011_archivobanco_userlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivobanco',
            name='userLog',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
