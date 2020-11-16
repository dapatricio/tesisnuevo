from django.urls import path
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path("", views.index, name="index"),
    path("informacion/", views.Informacion.as_view(), name="informacion"),
    path("proposito/", views.proposito, name="proposito"),
    path("contacto/", views.contacto, name="contacto"),
    path("registro/", views.registro, name="registro"),
    path(
        "login/actualizar/<int:pk>/", views.UpdateUserView.as_view(), name="actualizar"
    ),
]

from .cuestionario import *

# Urls Cuestionario
urlpatterns += [
    path(
        route="cuestionario/categoria/",
        view=CategoriaTemplateView.as_view(),
        name="categoria",
    ),
    path(
        route="cuestionario/historico/",
        view=HistorialTemplateView.as_view(),
        name="historico",
    ),
    path(
        route="cuestionario/informe/<str:area>/<slug:slug>/",
        view=repuestas_usuario,
        name="informe_area",
    ),
    path(
        route="login/cuestionario/<int:pk>/<slug:slug>-<str:uuid>/",
        view=cuestionarios,
        name="cuestionario",
    ),
    path(
        route="cuestionario/respuestas",
        view=repuestas_usuario,
        name="repuestas_usuario",
    ),
    path(
        route="pregunta/ajax/<int:id_preguntas>/<str:cuestionario>/<str:tipo>/",
        view=pregunta_ajax,
        name="pregunta_ajax",
    ),
]
