"""Template tags"""

# Django
from django import template

from appWeb.models import HistoricoEvaluacion

register = template.Library()


@register.filter(name="status_cuestionario")
@register.simple_tag
def status_cuestionario(value, user):
    instance = HistoricoEvaluacion.objects.filter(id_usr=user, code_uuid=value)
    return instance.exists()
