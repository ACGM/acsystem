# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0016_auto_20150201_0323'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivoBancoNomina',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bancoAsign', models.CharField(max_length=5)),
                ('tipoServicio', models.CharField(max_length=2)),
                ('envio', models.CharField(max_length=4)),
                ('secuencia', models.PositiveIntegerField()),
                ('datetimeServer', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='autorizador',
            options={'ordering': ['usuario'], 'verbose_name_plural': 'Config 3.1) Autorizadores'},
        ),
        migrations.AlterModelOptions(
            name='banco',
            options={'ordering': ['nombre'], 'verbose_name_plural': 'Config 2.1) Bancos'},
        ),
        migrations.AlterModelOptions(
            name='categoriaprestamo',
            options={'ordering': ['descripcion'], 'verbose_name': 'Categoria de Prestamo', 'verbose_name_plural': 'Config 6.1) Categorias de Prestamos'},
        ),
        migrations.AlterModelOptions(
            name='cobeneficiario',
            options={'ordering': ['nombre'], 'verbose_name': 'Config 1) Co-Beneficiario', 'verbose_name_plural': 'Config 1.2) Co-Beneficiarios'},
        ),
        migrations.AlterModelOptions(
            name='cobrador',
            options={'ordering': ['usuario'], 'verbose_name_plural': 'Config 3.2) Cobradores'},
        ),
        migrations.AlterModelOptions(
            name='cuotaahorrosocio',
            options={'ordering': ['socio'], 'verbose_name': 'Config 1) Cuota Ahorro Socio', 'verbose_name_plural': 'Config 1.3) Cuotas Ahorros Socios'},
        ),
        migrations.AlterModelOptions(
            name='cuotaordenes',
            options={'ordering': ['-montoDesde'], 'verbose_name': 'Cuota de Ordenes', 'verbose_name_plural': 'Config 6.3) Cuotas de Ordenes'},
        ),
        migrations.AlterModelOptions(
            name='cuotaprestamo',
            options={'ordering': ['-montoDesde'], 'verbose_name': 'Cuota de Prestamo', 'verbose_name_plural': 'Config 6.2) Cuotas de Prestamos'},
        ),
        migrations.AlterModelOptions(
            name='departamento',
            options={'ordering': ['descripcion'], 'verbose_name_plural': 'Config 1.4) Departamentos'},
        ),
        migrations.AlterModelOptions(
            name='distrito',
            options={'ordering': ['descripcion'], 'verbose_name_plural': 'Config 2.5) Distritos'},
        ),
        migrations.AlterModelOptions(
            name='documentocuentas',
            options={'ordering': ['documento', 'cuenta'], 'verbose_name': 'Documento relacionado a Cuentas', 'verbose_name_plural': 'Config 7.2) Documentos relacionados a Cuentas'},
        ),
        migrations.AlterModelOptions(
            name='empresa',
            options={'verbose_name_plural': 'Config 2.2) Empresas'},
        ),
        migrations.AlterModelOptions(
            name='localidad',
            options={'ordering': ['descripcion'], 'verbose_name_plural': 'Config 2.6) Localidades'},
        ),
        migrations.AlterModelOptions(
            name='opcion',
            options={'ordering': ['descripcion'], 'verbose_name_plural': 'Config 3.3) Opciones'},
        ),
        migrations.AlterModelOptions(
            name='perfil',
            options={'ordering': ['perfilCod'], 'verbose_name_plural': 'Config 3.4) Perfiles'},
        ),
        migrations.AlterModelOptions(
            name='periodo',
            options={'ordering': ['-agno'], 'verbose_name_plural': 'Config 7.3) Periodos'},
        ),
        migrations.AlterModelOptions(
            name='producto',
            options={'ordering': ['descripcion'], 'verbose_name_plural': 'Config 4.1) Productos'},
        ),
        migrations.AlterModelOptions(
            name='representante',
            options={'verbose_name_plural': 'Config 2.3) Representantes'},
        ),
        migrations.AlterModelOptions(
            name='socio',
            options={'ordering': ['codigo'], 'verbose_name': 'Config 1) Socio', 'verbose_name_plural': 'Config 1.1) Socios'},
        ),
        migrations.AlterModelOptions(
            name='suplidor',
            options={'ordering': ['nombre'], 'verbose_name_plural': 'Config 4.3) Suplidores'},
        ),
        migrations.AlterModelOptions(
            name='tipodocumento',
            options={'ordering': ['descripcion'], 'verbose_name_plural': 'Config 7.1) Tipos de Documentos'},
        ),
        migrations.AlterModelOptions(
            name='tiposuplidor',
            options={'ordering': ['descripcion'], 'verbose_name': 'Tipo de Suplidor', 'verbose_name_plural': 'Config 4.4) Tipos de Suplidores'},
        ),
        migrations.AlterModelOptions(
            name='unidad',
            options={'verbose_name': 'Unidad', 'verbose_name_plural': 'Config 4.2) Unidades'},
        ),
        migrations.AddField(
            model_name='autorizador',
            name='clave',
            field=models.CharField(default=b'', max_length=4),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaInicioAhorro',
            field=models.DateField(default=datetime.datetime(2015, 2, 1, 21, 3, 49, 491066), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaModificacion',
            field=models.DateField(default=datetime.datetime(2015, 2, 1, 21, 3, 49, 491091), auto_now=True),
            preserve_default=True,
        ),
    ]
