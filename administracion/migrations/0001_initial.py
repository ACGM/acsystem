# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cuenta', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Autorizador',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetimeServer', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['usuario'],
                'verbose_name_plural': 'Autorizadores',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=25)),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['nombre'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CategoriaPrestamo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=150)),
                ('montoDesde', models.DecimalField(verbose_name=b'Monto Desde', max_digits=18, decimal_places=2, blank=True)),
                ('montoHasta', models.DecimalField(verbose_name=b'Monto Hasta', max_digits=18, decimal_places=2, blank=True)),
                ('tipo', models.CharField(max_length=2, choices=[(b'OD', b'Orden de Despacho'), (b'PR', b'Prestamo'), (b'SC', b'SuperCoop')])),
                ('interesAnualSocio', models.DecimalField(null=True, verbose_name=b'Intereses Anual Socio', max_digits=6, decimal_places=2, blank=True)),
                ('interesAnualEmpleado', models.DecimalField(null=True, verbose_name=b'Intereses Anual Empleado', max_digits=6, decimal_places=2, blank=True)),
                ('interesAnualDirectivo', models.DecimalField(null=True, verbose_name=b'Intereses Anual Directivo', max_digits=6, decimal_places=2, blank=True)),
                ('datetimeServer', models.DateTimeField(auto_now_add=True)),
                ('userLog', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['descripcion'],
                'verbose_name': 'Categoria de Prestamo',
                'verbose_name_plural': 'Categorias de Prestamos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CoBeneficiario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=150)),
                ('direccion', models.TextField(null=True, blank=True)),
                ('sector', models.CharField(max_length=150, null=True, blank=True)),
                ('ciudad', models.CharField(max_length=100, null=True, blank=True)),
                ('cedula', models.CharField(max_length=15, null=True, blank=True)),
                ('telefono', models.CharField(max_length=100, null=True, blank=True)),
                ('celular', models.CharField(max_length=100, null=True, blank=True)),
                ('parentesco', models.CharField(default=b'O', max_length=1, choices=[(b'C', b'Conyugue'), (b'H', b'Hijo(a)'), (b'T', b'Tio(a)'), (b'A', b'Abuelo(a)'), (b'O', b'Otro')])),
            ],
            options={
                'ordering': ['nombre'],
                'verbose_name': 'Co-Beneficiario',
                'verbose_name_plural': 'Co-Beneficiarios',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cobrador',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('usuario', models.CharField(max_length=10)),
                ('datetimeServer', models.DateTimeField(auto_now_add=True)),
                ('userLog', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['usuario'],
                'verbose_name_plural': 'Cobradores',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CuotaAhorroSocio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cuotaAhorroQ1', models.DecimalField(null=True, verbose_name=b'Cuota Ahorro Q1', max_digits=18, decimal_places=2, blank=True)),
                ('cuotaAhorroQ2', models.DecimalField(null=True, verbose_name=b'Cuota Ahorro Q2', max_digits=18, decimal_places=2, blank=True)),
            ],
            options={
                'ordering': ['socio'],
                'verbose_name': 'Cuota Ahorro Socio',
                'verbose_name_plural': 'Cuotas Ahorros Socios',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CuotaOrdenes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('montoDesde', models.DecimalField(verbose_name=b'Monto Desde', max_digits=18, decimal_places=2)),
                ('montoHasta', models.DecimalField(verbose_name=b'Monto Hasta', max_digits=18, decimal_places=2)),
                ('cantidadQuincenas', models.PositiveIntegerField(verbose_name=b'Cantidad de Quincenas')),
                ('cantidadMeses', models.PositiveIntegerField(verbose_name=b'Cnatidad de Meses')),
                ('datetimeServer', models.DateTimeField(auto_now_add=True)),
                ('userLog', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-montoDesde'],
                'verbose_name': 'Cuota de Ordenes',
                'verbose_name_plural': 'Cuotas de Ordenes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CuotaPrestamo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('montoDesde', models.DecimalField(verbose_name=b'Monto Desde', max_digits=18, decimal_places=2)),
                ('montoHasta', models.DecimalField(verbose_name=b'Monto Hasta', max_digits=18, decimal_places=2)),
                ('cantidadQuincenas', models.PositiveIntegerField(verbose_name=b'Cantidad de Quincenas')),
                ('cantidadMeses', models.PositiveIntegerField(verbose_name=b'Cantidad de Meses')),
                ('datetimeServer', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-montoDesde'],
                'verbose_name': 'Cuota de Prestamo',
                'verbose_name_plural': 'Cuotas de Prestamos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('centroCosto', models.CharField(max_length=10, verbose_name=b'Centro de Costo')),
                ('descripcion', models.CharField(max_length=150)),
            ],
            options={
                'ordering': ['descripcion'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Distrito',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=150)),
            ],
            options={
                'ordering': ['descripcion'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentoCuentas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accion', models.CharField(max_length=1, choices=[(b'D', b'Debito'), (b'C', b'Credito')])),
                ('cuenta', models.ForeignKey(to='cuenta.Cuentas')),
            ],
            options={
                'ordering': ['documento', 'cuenta'],
                'verbose_name': 'Documento relacionado a Cuentas',
                'verbose_name_plural': 'Documentos relacionados a Cuentas',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Localidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=150)),
            ],
            options={
                'ordering': ['descripcion'],
                'verbose_name_plural': 'Localidades',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Opcion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=80)),
                ('tipo', models.CharField(default=b'P', max_length=1, choices=[(b'P', b'Principal'), (b'S', b'Secundario')])),
            ],
            options={
                'ordering': ['descripcion'],
                'verbose_name_plural': 'Opciones',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('perfilCod', models.CharField(unique=True, max_length=10, verbose_name=b'Codigo Perfil')),
                ('opcion', models.ForeignKey(to='administracion.Opcion')),
            ],
            options={
                'ordering': ['perfilCod'],
                'verbose_name_plural': 'Perfiles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mes', models.CharField(default=b'01', max_length=2, choices=[(b'01', b'Enero'), (b'02', b'Febrero'), (b'03', b'Marzo'), (b'04', b'Abril'), (b'05', b'Mayo'), (b'06', b'Junio'), (b'07', b'Julio'), (b'08', b'Agosto'), (b'09', b'Septiembre'), (b'10', b'Octubre'), (b'11', b'Noviembre'), (b'12', b'Diciembre')])),
                ('agno', models.CharField(max_length=4, verbose_name=b'Agno')),
                ('estatus', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Activo'), (b'C', b'Cerrado')])),
            ],
            options={
                'ordering': ['-agno'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=10)),
                ('descripcion', models.CharField(max_length=80)),
                ('precio', models.DecimalField(max_digits=18, decimal_places=2)),
                ('costo', models.DecimalField(null=True, max_digits=18, decimal_places=2, blank=True)),
                ('foto', models.ImageField(null=True, upload_to=b'productos', blank=True)),
                ('datetimeServer', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['descripcion'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Representante',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=150)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Socio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.IntegerField()),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('direccion', models.TextField(blank=True)),
                ('sector', models.CharField(max_length=150, blank=True)),
                ('telefono', models.CharField(max_length=150, blank=True)),
                ('celular', models.CharField(max_length=150, blank=True)),
                ('ciudad', models.CharField(max_length=150, blank=True)),
                ('cedula', models.CharField(max_length=20, blank=True)),
                ('sexo', models.CharField(default=b'M', max_length=1, choices=[(b'M', b'Masculino'), (b'F', b'Femenino')])),
                ('estadoCivil', models.CharField(default=b'S', max_length=1, verbose_name=b'Estado Civil', choices=[(b'S', b'Soltero(a)'), (b'C', b'Casado(a)'), (b'U', b'Union Libre')])),
                ('pasaporte', models.CharField(max_length=20, verbose_name=b'Pasaporte No.', blank=True)),
                ('carnetNumero', models.IntegerField(verbose_name=b'Carnet Numero')),
                ('fechaIngresoCoop', models.DateField(verbose_name=b'Fecha de Ingreso Coop.')),
                ('fechaIngresoEmpresa', models.DateField(verbose_name=b'Fecha de Ingreso Empresa')),
                ('correo', models.EmailField(max_length=75, blank=True)),
                ('estatus', models.CharField(default=b'S', max_length=2, choices=[(b'S', b'Socio'), (b'E', b'Empleado'), (b'I', b'Inactivo')])),
                ('salario', models.DecimalField(max_digits=18, decimal_places=2)),
                ('cuentaBancaria', models.CharField(max_length=20, verbose_name=b'Cuenta Bancaria', blank=True)),
                ('foto', models.ImageField(null=True, upload_to=b'administracion', blank=True)),
                ('nombreCompleto', models.CharField(verbose_name=b'Nombre Completo', max_length=200, editable=False)),
                ('datetime_server', models.DateTimeField(auto_now_add=True)),
                ('departamento', models.ForeignKey(to='administracion.Departamento')),
                ('distrito', models.ForeignKey(to='administracion.Distrito')),
                ('user_log', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['codigo'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Suplidor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipoIdentificacion', models.CharField(default=b'C', max_length=1, choices=[(b'C', b'Cedula'), (b'R', b'RNC')])),
                ('cedulaRNC', models.CharField(unique=True, max_length=25)),
                ('nombre', models.CharField(max_length=80)),
                ('direccion', models.TextField(blank=True)),
                ('sector', models.CharField(max_length=100, blank=True)),
                ('ciudad', models.CharField(max_length=100, blank=True)),
                ('contacto', models.CharField(max_length=150, blank=True)),
                ('telefono', models.CharField(max_length=50, blank=True)),
                ('fax', models.CharField(max_length=50, blank=True)),
                ('intereses', models.DecimalField(default=0, null=True, max_digits=5, decimal_places=2, blank=True)),
                ('clase', models.CharField(default=b'N', max_length=1, choices=[(b'N', b'Normal'), (b'S', b'SuperCoop')])),
                ('datetimeServer', models.DateTimeField(auto_now_add=True)),
                ('auxiliar', models.ForeignKey(to='cuenta.Auxiliares', null=True)),
            ],
            options={
                'ordering': ['nombre'],
                'verbose_name_plural': 'Suplidores',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoDocumento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=4)),
                ('descripcion', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['descripcion'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoNCGlobal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(default=b'', max_length=1, choices=[(b'1', b'NCG'), (b'2', b'NCG2')])),
                ('descripcion', models.CharField(max_length=150)),
                ('cuenta', models.ForeignKey(to='cuenta.Cuentas')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoSuplidor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['descripcion'],
                'verbose_name': 'Tipo de Suplidor',
                'verbose_name_plural': 'Tipos de Suplidores',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Unidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=20)),
                ('nota', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Unidad',
                'verbose_name_plural': 'Unidades',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='suplidor',
            name='tipoSuplidor',
            field=models.ForeignKey(to='administracion.TipoSuplidor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='suplidor',
            name='userLog',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='producto',
            name='unidad',
            field=models.ForeignKey(to='administracion.Unidad'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='producto',
            name='userLog',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='documentocuentas',
            name='documento',
            field=models.ForeignKey(to='administracion.TipoDocumento'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='distrito',
            name='localidad',
            field=models.ForeignKey(to='administracion.Localidad'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cuotaahorrosocio',
            name='socio',
            field=models.ForeignKey(to='administracion.Socio'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cobeneficiario',
            name='socio',
            field=models.ForeignKey(to='administracion.Socio'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='autorizador',
            name='perfil',
            field=models.ForeignKey(to='administracion.Perfil'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='autorizador',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
