from django.urls import path
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path("", views.index, name="index"),
    path("informacion/", views.informacion, name="informacion"),
    path("proposito/", views.proposito, name="proposito"),
    path("contacto/", views.contacto, name="contacto"),
    path("registro/", views.registro, name="registro"),
    path("login/actualizar/<int:pk>/", views.UpdateUserView.as_view(), name="actualizar"),
    path("login/cuestionario/", views.cuestionarios, name="cuestionario"),
    path("cuestionario/respuestas", views.repuestas_usuario, name="repuestas_usuario"),
    path(
        "pregunta/ajax/<int:id_preguntas>/<int:cuestionario>/",
        views.pregunta_ajax,
        name="pregunta_ajax",
    ),
]
