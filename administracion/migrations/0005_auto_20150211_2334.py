# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0004_remove_userextra_prueba'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userextra',
            unique_together=set([('usuario', 'localidad', 'perfil')]),
        ),
    ]
