from django.contrib import admin
from django.contrib.auth.models import Group
from . import models

from appWeb.models import Pregunta, Respuesta
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


class CompetenciaAdmin(admin.ModelAdmin):
    inlines = [RSubidaInline]
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
        "id_competencia",
    )


class RecomendacionAdmin(admin.ModelAdmin):
    list_display = (
        "recomendacion",
        "valor",
        "id_competencia",
    )


class RtaUsrAdmin(admin.ModelAdmin):
    list_display = (
        "rtaUser",
        "id_pregunta",
        "id_usr",
    )


class NivelAdmin(admin.ModelAdmin):
    list_display = (
        "nivel",
        "id_competencia",
        "id_dependencia",
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
# _register(models.Usuario, UsuarioAdmin)
_register(models.Pregunta, PreguntaAdmin)
_register(models.Recomendacion, RecomendacionAdmin)
_register(models.Respuesta, RespuestaAdmin)
_register(models.RtaUsr, RtaUsrAdmin)
_register(models.Nivel, NivelAdmin)

admin.site.unregister(Group)

admin.site.register(models.Profile)
admin.site.register(models.HistoricoEvaluacion)
