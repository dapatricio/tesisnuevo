from django.contrib import admin
from django.contrib.auth.models import Group
from . import models

from appWeb.models import Pregunta, Respuesta, RespuestaCuestionarioGeneral
from image_cropping import ImageCroppingMixin

# Register your models here.


class AreaAdmin(admin.ModelAdmin):
    list_display = ("nombArea",)


class Area_CompetenciaAdmin(admin.ModelAdmin):
    list_display = (
        "nombAreaCompetencia",
        "detalle_area_competencia",
    )


class TipoCuestAdmin(admin.ModelAdmin):
    list_display = ("nombCuest",)


class TipoDepAdmin(admin.ModelAdmin):
    list_display = ("tipo_dep",)


class TipoUsrAdmin(admin.ModelAdmin):
    list_display = ("tipo_usuario",)


class DependenciaAdmin(admin.ModelAdmin):
    list_display = (
        "nombDependencia",
        "id_tipoDep",
        "id_area",
    )

    list_filter = (
        "id_tipoDep",
        "id_area",
    )


class RSubidaInline(admin.StackedInline):
    model = models.Recomendaciones
    extra = 1

class RSubidaInline2(admin.StackedInline):
    model = models.Nivel
    extra = 2

class CompetenciaAdmin(admin.ModelAdmin):
    inlines = [RSubidaInline, RSubidaInline2]
    list_display = (
        "nombCompetencia",
        "detalle_competencia",
        "id_area_competencia",
    )


# class UsuarioAdmin(admin.ModelAdmin):
# 	list_display=(
# 		'nombUsuario',
# 		'cedula',
# 		'correo',
# 		'clave',
# 		'id_dependencia',
# 		'id_tipoUsr',
# 	)


class RespuestaAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = (
        "respuesta",
        "valorRta",
        "id_pregunta",
    )


class RespuestaInline(ImageCroppingMixin, admin.StackedInline):
    model = Respuesta
    extra = 4


class PreguntaAdmin(admin.ModelAdmin):
    inlines = [RespuestaInline]

    list_display = (
        "pregunta",
        "ayuda",
        "id_tipoCuest",
    )


class RecomendacionAdmin(admin.ModelAdmin):
    list_display = (
        "recomendacion",
        "valor",
        "id_competencia",
    )


class RtaUsrAdmin(admin.ModelAdmin):
    list_display = (
        "id_usr",
        "rtaUser",
        "id_pregunta", 
    )

class NivelAdmin(admin.ModelAdmin):
    list_display = (
        "nivel",
        "id_competencia",
        "id_dependencia",
    )


class RespuestaCuestionarioGeneralInline(ImageCroppingMixin, admin.StackedInline):
    model = RespuestaCuestionarioGeneral
    extra = 4


class PreguntaCuestionarioGeneralAdmin(admin.ModelAdmin):
    list_display = ("id", "pregunta", "ayuda")
    inlines = [RespuestaCuestionarioGeneralInline]


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.Area, AreaAdmin)
_register(models.Area_Competencia, Area_CompetenciaAdmin)
_register(models.TipoCuest, TipoCuestAdmin)
_register(models.TipoDep, TipoDepAdmin)
_register(models.TipoUsr, TipoUsrAdmin)
_register(models.Dependencia, DependenciaAdmin)
_register(models.Competencia, CompetenciaAdmin)
# _register(models.Usuario, UsuarioAdmin)
_register(models.Pregunta, PreguntaAdmin)
_register(models.Recomendacion, RecomendacionAdmin)
_register(models.Respuesta, RespuestaAdmin)
_register(models.RtaUsr, RtaUsrAdmin)
_register(models.Nivel, NivelAdmin)
_register(models.PreguntaCuestionarioGeneral, PreguntaCuestionarioGeneralAdmin)

#admin.site.unregister(Group)

admin.site.register(models.Profile)
admin.site.register(models.HistoricoEvaluacion)
admin.site.register(models.RtaUsrGeneral)
