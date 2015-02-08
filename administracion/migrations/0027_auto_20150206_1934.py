# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administracion', '0026_auto_20150205_0348'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivoBancoDetailN',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipoRegistro', models.CharField(max_length=1)),
                ('idCompania', models.CharField(max_length=15)),
                ('secuencia', models.CharField(max_length=7)),
                ('secuenciaTrans', models.CharField(max_length=7)),
                ('cuentaDestino', models.CharField(max_length=20)),
                ('tipoCuentaDestino', models.CharField(max_length=1)),
                ('monedaDestino', models.CharField(default=b'214', max_length=3)),
                ('codBancoDestino', models.CharField(default=b'10101070', max_length=8)),
                ('digiVerBancoDestino', models.CharField(default=b'8', max_length=1)),
                ('codigoOperacion', models.CharField(default=b'22', max_length=2)),
                ('montoTransaccion', models.CharField(max_length=13)),
                ('tipoIdentificacion', models.CharField(default=b'CE', max_length=2)),
                ('identificacion', models.CharField(max_length=15)),
                ('nombre', models.CharField(default=b'', max_length=35)),
                ('numeroReferencia', models.CharField(default=b'', max_length=12)),
                ('descrpEstadoDestino', models.CharField(default=b'', max_length=40)),
                ('fechaVencimiento', models.CharField(default=b'', max_length=4)),
                ('formaContacto', models.CharField(default=b' ', max_length=1)),
                ('emailBenef', models.CharField(default=b'', max_length=40)),
                ('faxTelefonoBenef', models.CharField(default=b'', max_length=12)),
                ('filler', models.CharField(default=b'00', max_length=2)),
                ('numeroAut', models.CharField(default=b'', max_length=15)),
                ('codRetornoRemoto', models.CharField(default=b'   ', max_length=3)),
                ('codRazonRemoto', models.CharField(default=b'   ', max_length=3)),
                ('codRazonInterno', models.CharField(default=b'   ', max_length=3)),
                ('procTransaccion', models.CharField(default=b' ', max_length=1)),
                ('estatusTransaccion', models.CharField(default=b' ', max_length=2)),
                ('filler2', models.CharField(default=b'', max_length=52)),
                ('lineaFormateadaN', models.CharField(max_length=320)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArchivoBancoDetailR',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipoRegistro', models.CharField(default=b'R', max_length=1)),
                ('idCompania', models.CharField(max_length=15)),
                ('secuencia', models.CharField(max_length=7)),
                ('secuenciaTrans', models.CharField(max_length=7)),
                ('numeroCtaDestino', models.CharField(max_length=20)),
                ('numeroDocumento', models.CharField(max_length=15)),
                ('tipoDocumento', models.CharField(max_length=2)),
                ('fechaDocumento', models.CharField(max_length=8)),
                ('montoDocumento', models.CharField(max_length=13)),
                ('montoDescuento', models.CharField(max_length=11)),
                ('montoImpuesto', models.CharField(max_length=11)),
                ('netoDocumento', models.CharField(max_length=13)),
                ('descripcion', models.CharField(max_length=50)),
                ('filler', models.CharField(max_length=146, blank=True)),
                ('lineaFormateadaR', models.CharField(max_length=319)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArchivoBancoHeader',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipoRegistro', models.CharField(max_length=1)),
                ('idCompania', models.CharField(max_length=15)),
                ('nombreCompania', models.CharField(max_length=35)),
                ('secuencia', models.CharField(max_length=7)),
                ('tipoServicio', models.CharField(max_length=2)),
                ('fechaEfectiva', models.CharField(max_length=8)),
                ('cantidadDB', models.CharField(max_length=11)),
                ('montoTotalDB', models.CharField(max_length=13)),
                ('cantidadCR', models.CharField(max_length=11)),
                ('montoTotalCR', models.CharField(max_length=13)),
                ('numeroAfiliacion', models.CharField(max_length=15)),
                ('fecha', models.CharField(max_length=8)),
                ('hora', models.CharField(max_length=4)),
                ('correo', models.CharField(max_length=40)),
                ('estatus', models.CharField(max_length=1)),
                ('cuentaEmpresa', models.CharField(max_length=1)),
                ('filler', models.CharField(max_length=107)),
                ('lineaFormateadaH', models.CharField(max_length=292)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserExtra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('localidad', models.ForeignKey(to='administracion.Localidad')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('usuario',),
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='ArchivoBancoNomina',
            new_name='ArchivoBanco',
        ),
        migrations.AddField(
            model_name='socio',
            name='tipoCuentaBancaria',
            field=models.CharField(default=b'1', max_length=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='suplidor',
            name='correo',
            field=models.CharField(max_length=40, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaInicioAhorro',
            field=models.DateField(default=datetime.datetime(2015, 2, 6, 19, 34, 24, 782969), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuotaahorrosocio',
            name='fechaModificacion',
            field=models.DateField(default=datetime.datetime(2015, 2, 6, 19, 34, 24, 782994), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='suplidor',
            name='ciudad',
            field=models.CharField(max_length=40, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='suplidor',
            name='contacto',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='suplidor',
            name='fax',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='suplidor',
            name='sector',
            field=models.CharField(max_length=40, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='suplidor',
            name='telefono',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
    ]
