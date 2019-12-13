from django.contrib import admin
from . import models
# Register your models here.

class AreaAdmin(admin.ModelAdmin):
	list_display=(
		'nombArea',
	)

class Area_CompetenciaAdmin(admin.ModelAdmin):
	list_display=(
		'nombAreaCompetencia', 
		'detalle_area_competencia',
	)

class TipoCuestAdmin(admin.ModelAdmin):
	list_display=(
		'nombCuest',
	)		

class TipoDepAdmin(admin.ModelAdmin):
	list_display=(
		'tipo_dep',
	)

class TipoUsrAdmin(admin.ModelAdmin):
	list_display=(
		'tipo_usuario',
	)

class DependenciaAdmin(admin.ModelAdmin):
	list_display=(
		'nombDependencia', 
		'id_tipoDep', 
		'id_area',
	)

class CompetenciaAdmin(admin.ModelAdmin):
	list_display=(
		'nombCompetencia', 
		'detalle_competencia', 
		'id_area_competencia',
	)

class UsuarioAdmin(admin.ModelAdmin):
	list_display=(
		'nombUsuario', 
		'cedula', 
		'correo', 
		'clave', 
		'id_dependencia', 
		'id_tipoUsr',
	)

class PreguntaAdmin(admin.ModelAdmin):
	list_display=(
		'pregunta', 
		'ayuda', 
		'id_tipoCuest', 
		'id_competencia',
	)

class RecomendacionAdmin(admin.ModelAdmin):
	list_display=(
		'recomendacion', 
		'valor', 
		'id_pregunta',
	)

class RespuestaAdmin(admin.ModelAdmin):
	list_display=(
		'respuesta', 
		'valorRta', 
		'id_pregunta',
	)

class RtaUsrAdmin(admin.ModelAdmin):
	list_display=(
		'rtaUser', 
		'id_pregunta', 
		'id_usr',
	)

class NivelAdmin(admin.ModelAdmin):
	list_display=(
		'nivel', 
		'id_competencia', 
		'id_dependencia',
	)

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(models.Area, AreaAdmin)
_register(models.Area_Competencia, Area_CompetenciaAdmin)
_register(models.TipoCuest, TipoCuestAdmin)
_register(models.TipoDep, TipoDepAdmin)
_register(models.TipoUsr, TipoUsrAdmin)
_register(models.Dependencia, DependenciaAdmin)
_register(models.Competencia, CompetenciaAdmin)
_register(models.Usuario, UsuarioAdmin)
_register(models.Pregunta, PreguntaAdmin)
_register(models.Recomendacion, RecomendacionAdmin)
_register(models.Respuesta, RespuestaAdmin)
_register(models.RtaUsr, RtaUsrAdmin)
_register(models.Nivel, NivelAdmin)