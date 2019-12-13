from django.db import models

# Create your models here.

class Area(models.Model):
	id_area=models.AutoField(primary_key=True)
	nombArea=models.CharField(max_length=150, verbose_name='Nombre Areas')

	class Meta:
		db_table='area'

	def __str__(self):
		return u'%s' %self.nombArea

class Area_Competencia(models.Model):
	id_area_competencia=models.AutoField(primary_key=True)
	nombAreaCompetencia=models.CharField(max_length=150, verbose_name='Nombre Area de Competencia')
	detalle_area_competencia=models.CharField(max_length=500, verbose_name='Descripcion Area de Competencia')

	class Meta:
		db_table='area_competencia'

	def __str__(self):
		return u'%s' %self.nombAreaCompetencia

class TipoCuest(models.Model):
	id_tipoCuest=models.AutoField(primary_key=True)
	nombCuest=models.CharField(max_length=150, verbose_name='Tipo de Cuestionario')

	class Meta:
		db_table='tipoCuest'

	def __str__(self):
		return u'%s' %self.nombCuest	

class TipoDep(models.Model):
	id_tipoDep=models.AutoField(primary_key=True)
	tipo_dep=models.CharField(max_length=150, verbose_name='Nombre Tipo de Dependencia')

	class Meta:
		db_table='tipoDep'

	def __str__(self):
		return u'%s' %self.tipo_dep	

class TipoUsr(models.Model):
	id_tipoUsr=models.AutoField(primary_key=True)
	tipo_usuario=models.CharField(max_length=150, verbose_name='Nombre Tipo de Usuario')

	class Meta:
		db_table='tipoUsr'

	def __str__(self):
		return u'%s' %self.tipo_usuario

class Dependencia(models.Model):
	id_dependencia=models.AutoField(primary_key=True)
	nombDependencia=models.CharField(max_length=150, verbose_name='Nombre Dependencia')

	id_tipoDep=models.ForeignKey(TipoDep, models.DO_NOTHING, db_column='id_tipoDep')
	id_area=models.ForeignKey(Area, models.DO_NOTHING, db_column='id_area')


	class Meta:
		db_table='dependencia'

	def __str__(self):
		return u'%s' %self.nombDependencia	

class Competencia(models.Model):
	id_competencia=models.AutoField(primary_key=True)
	nombCompetencia=models.CharField(max_length=75, verbose_name='Nombre Competencia')
	detalle_competencia=models.CharField(max_length=75, verbose_name='Descripcion Competencia')

	id_area_competencia=models.ForeignKey(Area_Competencia, models.DO_NOTHING, db_column='id_area_competencia')

	class Meta:
		db_table='competencia'

	def __str__(self):
		return u'%s' %self.nombCompetencia	

class Usuario(models.Model):
	id_usr=models.AutoField(primary_key=True)
	nombUsuario=models.CharField(max_length=150, verbose_name='Nombre Usuario')
	cedula=models.CharField(max_length=11, verbose_name='Cédula Usuario')
	correo=models.CharField(max_length=75, verbose_name='Correo Usuario')
	clave=models.CharField(max_length=75, verbose_name='Contraseña')
	codigo=models.CharField(max_length=75, verbose_name='Contraseña')
	estado_codigo=models.BooleanField()

	id_dependencia=models.ForeignKey(Dependencia, models.DO_NOTHING, db_column='id_dependencia')
	id_tipoUsr=models.ForeignKey(TipoUsr, models.DO_NOTHING, db_column='id_tipoUsr')

	class Meta:
		db_table='usuario'

	def __str__(self):
		return u'%s' %self.nombUsuario		

class Pregunta(models.Model):
	id_pregunta=models.AutoField(primary_key=True)
	pregunta=models.CharField(max_length=250, verbose_name='Pregunta')
	ayuda=models.CharField(max_length=250, verbose_name='Ayuda para la Pregunta')

	id_tipoCuest=models.ForeignKey(TipoCuest, models.DO_NOTHING, db_column='id_tipoCuest')
	id_competencia=models.ForeignKey(Competencia, models.DO_NOTHING, db_column='id_competencia')

	class Meta:
		db_table='pregunta'

	def __str__(self):
		return u'%s' %self.pregunta	

class Recomendacion(models.Model):
	id_recomendacion=models.AutoField(primary_key=True)
	recomendacion=models.CharField(max_length=500, verbose_name='Recomendación valor respuesta')
	valor=models.IntegerField()

	id_pregunta=models.ForeignKey(Pregunta, models.DO_NOTHING, db_column='id_pregunta')

	class Meta:
		db_table='recomendacion'

	def __str__(self):
		return u'%s' %self.recomendacion

class Respuesta(models.Model):
	id_respuesta=models.AutoField(primary_key=True)
	respuesta=models.CharField(max_length=150, verbose_name='Respuesta pregunta')
	valorRta=models.IntegerField()

	id_pregunta=models.ForeignKey(Pregunta, models.DO_NOTHING, db_column='id_pregunta')

	class Meta:
		db_table='respuesta'

	def __str__(self):
		return u'%s' %self.respuesta

class RtaUsr(models.Model):
	id_rtaUser=models.AutoField(primary_key=True)
	rtaUser=models.CharField(max_length=75, verbose_name='Respuesta usuario')

	id_pregunta=models.ForeignKey(Pregunta, models.DO_NOTHING, db_column='id_pregunta')
	id_usr=models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usr')

	class Meta:
		db_table='rtaUser'

	def __str__(self):
		return u'%s' %self.rtaUser

class Nivel(models.Model):
	id_nivel=models.AutoField(primary_key=True)
	nivel=models.IntegerField()

	id_competencia=models.ForeignKey(Competencia, models.DO_NOTHING, db_column='id_competencia')
	id_dependencia=models.ForeignKey(Dependencia, models.DO_NOTHING, db_column='id_dependencia')

	class Meta:
		db_table='nivel'

	def __str__(self):
		return u'%s' %self.nivel