from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('informacion/', views.informacion, name='informacion'),
    path('proposito/', views.proposito, name='proposito'),
    path('contacto/', views.contacto, name='contacto'),
]
