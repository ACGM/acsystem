# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nominacoop', '0004_auto_20150116_0244'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nominacooph',
            old_name='user_log',
            new_name='userLog',
        ),
    ]
