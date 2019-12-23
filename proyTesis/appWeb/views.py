from django.shortcuts import render, redirect
from .models import *
from .forms import UsuarioForm, ContactoForm
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponseRedirect


# Create your views here.
def index(request):
	return render(request, 'index.html')

def informacion(request):
	return render(request, 'informacion.html')

def proposito(request):
	return render(request, 'proposito.html')	

def contacto(request):
	if request.method == 'POST':
		contacto_form = ContactoForm(request.POST)
		if contacto_form.is_valid():
			asunto = 'Nueva consulta del Sistema de Encuestas'
			mensaje = contacto_form.cleaned_data['mensaje']
			mail = EmailMessage(asunto, mensaje, to=['andrews19aa@gmail.com'])
			mail.send()
		return HttpResponseRedirect('/')
	else:
		contacto_form = ContactoForm()

	return render(request, 'contacto.html', {'contacto_form':contacto_form})

def login(request):
	return render(request, 'login.html')

def registro(request):
	if request.method == 'POST':
		usuario_form = UsuarioForm(request.POST)
		if usuario_form.is_valid():
			usuario_form.save()
			return redirect('login')
	else:
		usuario_form = UsuarioForm()
	return render(request, 'registro.html', {'usuario_form':usuario_form})