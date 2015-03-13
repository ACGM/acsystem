# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('prestamos', '__first__'),
        ('administracion', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CargoCoop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=40)),
            ],
            options={
                'ordering': ['descripcion'],
                'verbose_name': 'Cargo Cooperativa',
                'verbose_name_plural': 'Cargos Cooperativa',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CuotasAhorrosEmpresa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valorAhorro', models.DecimalField(max_digits=12, decimal_places=2)),
                ('fecha', models.DateField(auto_now=True, null=True)),
                ('nomina', models.DateField(null=True)),
                ('estatus', models.CharField(default=b'P', max_length=1, choices=[(b'P', b'Pendiente'), (b'A', b'Aprobado')])),
                ('socio', models.ForeignKey(to='administracion.Socio')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CuotasPrestamosEmpresa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valorCapital', models.DecimalField(max_digits=12, decimal_places=2)),
                ('valorInteres', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('nomina', models.DateField(null=True)),
                ('fecha', models.DateField(auto_now=True, null=True)),
                ('estatus', models.CharField(default=b'P', max_length=1, choices=[(b'P', b'Pendiente'), (b'A', b'Aprobado')])),
                ('cuota', models.ForeignKey(to='prestamos.PagoCuotasPrestamo')),
                ('noPrestamo', models.ForeignKey(to='prestamos.MaestraPrestamo')),
                ('socio', models.ForeignKey(to='administracion.Socio')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DepartamentoCoop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=40)),
            ],
            options={
                'ordering': ['descripcion'],
                'verbose_name': 'Departamento Cooperativa',
                'verbose_name_plural': 'Departamentos Cooperativa',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmpleadoCoop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.PositiveIntegerField(max_length=6)),
                ('nombres', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50)),
                ('cedula', models.CharField(max_length=20)),
                ('direccion', models.TextField(null=True, blank=True)),
                ('sector', models.CharField(max_length=50, null=True, blank=True)),
                ('ciudad', models.CharField(max_length=40, null=True, blank=True)),
                ('telefono', models.CharField(max_length=40, null=True, blank=True)),
                ('fechaNac', models.DateField(null=True, verbose_name=b'Fecha de Nacimiento', blank=True)),
                ('lugarNac', models.CharField(max_length=50, null=True, verbose_name=b'Lugar de Nacimiento', blank=True)),
                ('estadoCivil', models.CharField(default=b'S', max_length=1, verbose_name=b'Estado Civil', choices=[(b'S', b'Soltero(a)'), (b'C', b'Casado(a)'), (b'U', b'Union Libre')])),
                ('sexo', models.CharField(default=b'M', max_length=1, choices=[(b'M', b'Masculino'), (b'F', b'Femenino')])),
                ('dependencias', models.PositiveIntegerField(null=True, blank=True)),
                ('fechaIngreso', models.DateField(auto_now=True, verbose_name=b'Fecha de Ingreso')),
                ('tipoContrato', models.CharField(default=b'F', max_length=1, verbose_name=b'Tipo de Contrato', choices=[(b'F', b'Fijo'), (b'T', b'Temporal')])),
                ('tipoCobro', models.CharField(default=b'Q', max_length=1, verbose_name=b'Tipo de Cobro', choices=[(b'F', b'Fijo'), (b'T', b'Temporal')])),
                ('tipoPago', models.CharField(default=b'B', max_length=1, verbose_name=b'Tipo de Pago', choices=[(b'E', b'Efectivo'), (b'C', b'Cheque'), (b'B', b'Banco')])),
                ('sueldoActual', models.DecimalField(verbose_name=b'Sueldo Actual', max_digits=18, decimal_places=2)),
                ('sueldoAnterior', models.DecimalField(null=True, verbose_name=b'Sueldo Anterior', max_digits=18, decimal_places=2, blank=True)),
                ('activo', models.BooleanField(default=True)),
                ('fechaSalida', models.DateField(null=True, verbose_name=b'Fecha de Salida', blank=True)),
                ('cargo', models.ForeignKey(to='nominacoop.CargoCoop')),
                ('departamento', models.ForeignKey(to='nominacoop.DepartamentoCoop')),
                ('empresa', models.ForeignKey(to='administracion.Empresa')),
            ],
            options={
                'ordering': ['codigo'],
                'verbose_name': 'Empleado Cooperativa',
                'verbose_name_plural': 'Empleados Cooperativa',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NominaCoopD',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('salario', models.DecimalField(max_digits=12, decimal_places=2)),
                ('isr', models.DecimalField(default=0, null=True, max_digits=12, decimal_places=2, blank=True)),
                ('afp', models.DecimalField(default=0, null=True, max_digits=12, decimal_places=2, blank=True)),
                ('ars', models.DecimalField(default=0, null=True, max_digits=12, decimal_places=2, blank=True)),
                ('cafeteria', models.DecimalField(default=0, null=True, max_digits=12, decimal_places=2, blank=True)),
                ('vacaciones', models.DecimalField(default=0, null=True, max_digits=12, decimal_places=2, blank=True)),
                ('otrosIngresos', models.DecimalField(default=0, null=True, max_digits=12, decimal_places=2, blank=True)),
                ('horasExtras', models.DecimalField(default=0, null=True, max_digits=12, decimal_places=2, blank=True)),
                ('descAhorros', models.DecimalField(default=0, null=True, max_digits=12, decimal_places=2, blank=True)),
                ('descPrestamos', models.DecimalField(default=0, null=True, max_digits=12, decimal_places=2, blank=True)),
                ('tipoPago', models.CharField(default=b'B', max_length=1, choices=[(b'E', b'Efectivo'), (b'C', b'Cheque'), (b'B', b'Banco')])),
                ('estatus', models.CharField(default=b'E', max_length=1, choices=[(b'P', b'Procesada'), (b'E', b'En proceso')])),
                ('empleado', models.ForeignKey(to='nominacoop.EmpleadoCoop')),
            ],
            options={
                'verbose_name': 'Nomina Detalles',
                'verbose_name_plural': 'Nominas Detalles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NominaCoopH',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fechaNomina', models.DateField()),
                ('fechaPago', models.DateField(null=True)),
                ('tipoPago', models.CharField(default=b'B', max_length=1, choices=[(b'E', b'Efectivo'), (b'C', b'Cheque'), (b'B', b'Banco')])),
                ('estatus', models.CharField(default=b'E', max_length=1, choices=[(b'P', b'Procesada'), (b'E', b'En proceso')])),
                ('quincena', models.PositiveIntegerField(default=1, choices=[(1, b'1ra. Quincena'), (2, b'2da. Quincena')])),
                ('nota', models.TextField(blank=True)),
                ('posteada', models.CharField(default=b'N', max_length=1)),
                ('fechaPosteo', models.DateField(auto_now=True, null=True)),
                ('datetime_server', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': 'Nomina Cabecera',
                'verbose_name_plural': 'Nominas Cabecera',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoNomina',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Tipo de Nomina',
                'verbose_name_plural': 'Tipos de Nominas',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='nominacooph',
            name='tipoNomina',
            field=models.ForeignKey(to='nominacoop.TipoNomina'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='nominacooph',
            name='userLog',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='nominacooph',
            unique_together=set([('fechaNomina', 'tipoNomina')]),
        ),
        migrations.AddField(
            model_name='nominacoopd',
            name='nomina',
            field=models.ForeignKey(to='nominacoop.NominaCoopH'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='nominacoopd',
            unique_together=set([('nomina', 'empleado')]),
        ),
    ]
