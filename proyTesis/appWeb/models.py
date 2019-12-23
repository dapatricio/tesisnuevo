from django.db import models
import hashlib
from django.contrib.auth.models import User
# Create your models here.
# 
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser

class Area(models.Model):
	id_area=models.AutoField(primary_key=True)
	nombArea=models.CharField(max_length=250, verbose_name='Nombre del área academica:')

	class Meta:
		verbose_name = "Áreas académica"
		db_table='area'

	def __str__(self):
		return u'%s' %self.nombArea

class Area_Competencia(models.Model):
	id_area_competencia=models.AutoField(primary_key=True)
	nombAreaCompetencia=models.CharField(max_length=250, verbose_name='Nombre del área de competencia:')
	detalle_area_competencia=models.CharField(max_length=500, verbose_name='Descripcion del área de competencia:')

	class Meta:
		verbose_name = "Áreas de competencia"
		db_table='area_competencia'

	def __str__(self):
		return u'%s' %self.nombAreaCompetencia

class TipoCuest(models.Model):
	id_tipoCuest=models.AutoField(primary_key=True)
	nombCuest=models.CharField(max_length=250, verbose_name='Tipo de cuestionario:')

	class Meta:
		db_table='tipoCuest'
		verbose_name = "Tipos de cuestionario"

	def __str__(self):
		
		return u'%s' %self.nombCuest	

class TipoDep(models.Model):
	id_tipoDep=models.AutoField(primary_key=True)
	tipo_dep=models.CharField(max_length=250, verbose_name='Nombre del tipo de dependencia:')

	class Meta:
		verbose_name = "Tipos de dependencia"
		db_table='tipoDep'

	def __str__(self):
		return u'%s' %self.tipo_dep	

class TipoUsr(models.Model):
	id_tipoUsr=models.AutoField(primary_key=True)
	tipo_usuario=models.CharField(max_length=250, verbose_name='Nombre del tipo de usuario:')

	class Meta:
		verbose_name = "Tipos de usuario"
		db_table='tipoUsr'

	def __str__(self):
		return u'%s' %self.tipo_usuario

class Dependencia(models.Model):
	id_dependencia=models.AutoField(primary_key=True)
	nombDependencia=models.CharField(max_length=250, verbose_name='Nombre de la dependencia:')

	id_tipoDep=models.ForeignKey(TipoDep, models.DO_NOTHING, db_column='id_tipoDep', verbose_name='Tipo de dependencia:')
	id_area=models.ForeignKey(Area, models.DO_NOTHING, db_column='id_area', verbose_name='Área academica:')


	class Meta:
		verbose_name = "Dependencias académica"
		db_table='dependencia'

	def __str__(self):
		return u'%s' %self.nombDependencia	

class Competencia(models.Model):
	id_competencia=models.AutoField(primary_key=True)
	nombCompetencia=models.CharField(max_length=250, verbose_name='Nombre de la competencia:')
	detalle_competencia=models.CharField(max_length=250, verbose_name='Descripción de la competencia:')

	id_area_competencia=models.ForeignKey(Area_Competencia, models.DO_NOTHING, db_column='id_area_competencia', verbose_name='Área de la competencia:')

	class Meta:
		verbose_name = "Competencias digitale"
		db_table='competencia'

	def __str__(self):
		return u'%s' %self.nombCompetencia	

class Usuario(models.Model):
  	id_usr=models.AutoField(primary_key=True)
  	nombUsuario=models.CharField(max_length=250, verbose_name='Nombres y Apellidos:')
  	cedula=models.CharField(max_length=11, verbose_name='Cédula usuario:')
  	correo=models.EmailField(max_length=75, verbose_name='Correo usuario:')
  	clave=models.CharField(max_length=75, verbose_name='Contraseña:')
  	codigo=models.CharField(max_length=75, verbose_name='Codigo:')
  	estado_codigo=models.BooleanField()

  	id_tipoUsr=models.ForeignKey(TipoUsr, models.DO_NOTHING, db_column='id_tipoUsr', verbose_name='Tipo de usuario:')
  	id_dependencia=models.ForeignKey(Dependencia, models.DO_NOTHING, db_column='id_dependencia', verbose_name='Dependencia:')

  	class Meta:
  		verbose_name='Usuario'
  		db_table='usuario'

  	def __str__(self):
  		return u'%s' %self.nombUsuario		

class Pregunta(models.Model):
	id_pregunta=models.AutoField(primary_key=True)

	id_competencia=models.ForeignKey(Competencia, models.DO_NOTHING, db_column='id_competencia', verbose_name='Competencia digital a la que pertenece:')
	id_tipoCuest=models.ForeignKey(TipoCuest, models.DO_NOTHING, db_column='id_tipoCuest', verbose_name='Tipo de cuestionario:')

	ayuda=models.CharField(max_length=250, verbose_name='Instrucción para la pregunta:')
	pregunta=models.CharField(max_length=250, verbose_name='Pregunta:')

	class Meta:
		verbose_name = "Pregunta"
		db_table='pregunta'

	def __str__(self):
		return u'%s' %self.pregunta	

class Recomendacion(models.Model):
	id_recomendacion=models.AutoField(primary_key=True)
	recomendacion=models.CharField(max_length=500, verbose_name='Recomendación del valor respuesta:')
	valor=models.IntegerField(verbose_name='Valor de la recomendación:')

	id_competencia=models.ForeignKey(Competencia, models.DO_NOTHING, db_column='id_competencia', verbose_name='Competencia a la que pertenece:')

	class Meta:
		verbose_name = "Recomendacióne"
		db_table='recomendacion'

	def __str__(self):
		return u'%s' %self.recomendacion

class Respuesta(models.Model):
	id_respuesta=models.AutoField(primary_key=True)
	respuesta=models.CharField(max_length=250, verbose_name='Respuesta pregunta:')
	valorRta=models.IntegerField(verbose_name='Valor de la respuesta:')

	id_pregunta=models.ForeignKey(Pregunta, models.DO_NOTHING, db_column='id_pregunta', verbose_name='Pregunta a la que pertenece:')

	class Meta:
		verbose_name = "Respuesta"
		db_table='respuesta'

	def __str__(self):
		return u'%s' %self.respuesta

class RtaUsr(models.Model):
	id_rtaUser=models.AutoField(primary_key=True)
	rtaUser=models.CharField(max_length=75, verbose_name='Respuesta usuario')

	id_pregunta=models.ForeignKey(Pregunta, models.DO_NOTHING, db_column='id_pregunta', verbose_name='Pregunta a la que pertenece:')
	id_usr = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usr', verbose_name='Respuesta realizada por:')

	class Meta:
		verbose_name = "Respuestas Usuario"
		db_table='rtaUser'

	def __str__(self):
		return u'%s' %self.rtaUser

class Nivel(models.Model):
	id_nivel=models.AutoField(primary_key=True)
	nivel=models.IntegerField(verbose_name='Nivel recomendado:')

	id_competencia=models.ForeignKey(Competencia, models.DO_NOTHING, db_column='id_competencia', verbose_name='Competencia digital:')
	id_dependencia=models.ForeignKey(Dependencia, models.DO_NOTHING, db_column='id_dependencia', verbose_name='Dependencia:')

	class Meta:
		verbose_name = "Niveles requerido"
		db_table='nivel'

	def __str__(self):
		return u'%s' %self.nivel