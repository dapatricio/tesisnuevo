from django.shortcuts import render
from .models import *
# Create your views here.
def index(request):
	return render(request, 'index.html')

def informacion(request):
	return render(request, 'informacion.html')

def proposito(request):
	return render(request, 'proposito.html')	

def contacto(request):
	return render(request, 'contacto.html')	

def login(request):
	return render(request, 'login.html')