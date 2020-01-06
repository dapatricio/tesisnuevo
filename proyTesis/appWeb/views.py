from django.shortcuts import render, redirect
from .models import *
from .forms import ContactoForm, UserForm, ProfileForm
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
			asunto = contacto_form.cleaned_data['asunto']
			mensaje = 'El mensaje indica:\n'+contacto_form.cleaned_data['mensaje']+'\n\n Enviado por: '+contacto_form.cleaned_data['nombre']+'\n Correo electrónico: '+contacto_form.cleaned_data['correo']
			mail = EmailMessage(asunto, mensaje, to=['dppenarreta@gmail.com'])
			mail.send()
		return HttpResponseRedirect('/')
	else:
		contacto_form = ContactoForm()

	return render(request, 'contacto.html', {'contacto_form':contacto_form})

def login(request):
	return render(request, 'login.html')

# def registro(request):
#  	if request.method == 'POST':
#  		usuario_form = UsuarioForm(request.POST)
#  		if usuario_form.is_valid():
#  			usuario_form.save()
#  			return redirect('login')
#  	else:
#  		usuario_form = UsuarioForm()
#  	return render(request, 'registro.html', {'usuario_form':usuario_form})

def registro(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('login')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'registro.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })