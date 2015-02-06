# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0025_auto_20150205_0320'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoriaproducto',
            options={'verbose_name_plural': 'Config 4.2) Categorias de Productos'},
        ),
        migrations.AlterModelOptions(
            name='suplidor',
            options={'ordering': ['nombre'], 'verbose_name_plural': 'Config 4.4) Suplidores'},
        ),
        migrations.AlterModelOptions(
            name='tiposuplidor',
            options={'ordering': ['descripcion'], 'verbose_name': 'Tipo de Suplidor', 'verbose_name_plural': 'Config 4.5) Tipos de Suplidores'},
        ),
        migrations.AlterModelOptions(
            name='unidad',
            options={'verbose_name': 'Unidad', 'verbose_name_plural': 'Config 4.3) Unidades'},
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaInicioAhorro',
            field=models.DateField(default=datetime.datetime(2015, 2, 5, 3, 48, 29, 724480), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaModificacion',
            field=models.DateField(default=datetime.datetime(2015, 2, 5, 3, 48, 29, 724504), auto_now=True),
            preserve_default=True,
        ),
    ]
