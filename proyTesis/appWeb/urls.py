from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

urlpatterns = [
    path("", views.index, name="index"),
    path("informacion/", views.informacion, name="informacion"),
    path("proposito/", views.proposito, name="proposito"),
    path("contacto/", views.contacto, name="contacto"),
    path("registro/", views.registro, name="registro"),
    path("login/cuestionario/", views.cuestionarios, name="cuestionario"),
    path(
        "pregunta/ajax/<int:id_preguntas>/<int:cuestionario>/",
        views.pregunta_ajax,
        name="pregunta_ajax",
    ),
]
