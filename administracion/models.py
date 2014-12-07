from django.db import models


# PRODUCTOS para registrarlos en la facturacion
class Producto(models.Model):
	unidades_choices = (('UN','Unidad'),('CA','Caja'),)

	codigo = models.CharField(max_length=10)
	descripcion = models.CharField(max_length=150)
	unidad = models.CharField(max_length=2, 
								choices=unidades_choices, 
								default=unidades_choices[0][0])
	precio = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
	costo = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
	foto = models.ImageField(upload_to='productos', blank=True)

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']


# Tipo de suplidores
class TipoSuplidor(models.Model):
	descripcion = models.CharField(max_length=100)

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']


# Suplidores/Proveedores registrados
class Suplidor(models.Model):
	nombre = models.CharField(max_length=150)
	direccion = models.TextField(blank=True)
	sector = models.CharField(max_length=100, blank=True)
	ciudad = models.CharField(max_length=100, blank=True)
	contacto = models.CharField(max_length=150, blank=True)
	telefono = models.CharField(max_length=50, blank=True)
	fax = models.CharField(max_length=50, blank=True)
	intereses = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
	tipo_suplidor = models.ForeignKey(TipoSuplidor)

	def __unicode__(self):
		return '%s' % (self.nombre)

	class Meta:
		ordering = ['nombre']


# Socios de la cooperativa
class Socio(model.Model):
	pass


# Categorias de Prestamos
class CategoriaPrestamo(models.Model):
	pass