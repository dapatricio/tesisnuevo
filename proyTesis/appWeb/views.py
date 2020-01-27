from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .forms import ContactoForm, UserForm, ProfileForm, UserLoginForm
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.shortcuts import render
from django.shortcuts import render, redirect

# from .forms import *
from .models import *
from datetime import datetime
from django.http import JsonResponse
import pytz, datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "index.html")


def informacion(request):
    return render(request, "informacion.html")


def proposito(request):
    return render(request, "proposito.html")


def contacto(request):
    if request.method == "POST":
        contacto_form = ContactoForm(request.POST)
        if contacto_form.is_valid():
            asunto = contacto_form.cleaned_data["asunto"]
            mensaje = (
                "El mensaje indica:\n"
                + contacto_form.cleaned_data["mensaje"]
                + "\n\n Enviado por: "
                + contacto_form.cleaned_data["nombre"]
                + "\n Correo electrónico: "
                + contacto_form.cleaned_data["correo"]
            )
            mail = EmailMessage(asunto, mensaje, to=["dppenarreta@gmail.com"])
            mail.send()
        return HttpResponseRedirect("/")
    else:
        contacto_form = ContactoForm()

    return render(request, "contacto.html", {"contacto_form": contacto_form})


# def login(request):
#     return render(request, "login.html")


def registro(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            usuario = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = usuario
            profile.save()
            return redirect("login")
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(
        request, "registro.html", {"user_form": user_form, "profile_form": profile_form}
    )


@login_required
def cuestionarios(request):
    lista = []
    profile = Profile.objects.get(user=request.user)
    ide_cuestionario = str(profile.id_tipoUsr.pk)
    categorias = TipoCuest.objects.filter(id_tipoUsr=profile.id_tipoUsr)
    contador, total = 0, 0
    if ("calificacion" + ide_cuestionario) not in request.session:
        request.session["bloqueo"] = "true"
        request.session["cuestionario_terminado" + ide_cuestionario] = False
        request.session["calificacion" + ide_cuestionario] = 0
        request.session["total" + ide_cuestionario] = total

    if ("cuestionario_iniciado" + ide_cuestionario) not in request.session:
        request.session["bloqueo"] = "true"
        request.session["calificacion" + ide_cuestionario] = 0
        request.session["cuestionario_terminado" + ide_cuestionario] = False
        for c in categorias:
            lista_preguntas = []
            preguntas = Pregunta.objects.filter(id_tipoCuest=c.pk).order_by("?")
            for d in preguntas:
                contador = contador + 1
                total = 1 + total
                lista_preguntas.append(
                    {
                        "contador": contador,
                        "id_preguntas": d.pk,
                        "llena": False,
                        "correcta": "false",
                        "opcion": 0,
                    }
                )
            lista.append(
                {"categorias": c.nombCuest, "preguntas": lista_preguntas,}
            )
            request.session["cuestionario_iniciado" + ide_cuestionario] = True
        # lista = json.dumps(list(lista), cls=DjangoJSONEncoder)
        request.session["total" + ide_cuestionario] = total
        total = 0
        request.session["lista" + ide_cuestionario] = lista

    # Aqui guardo la instancia para que se guarde la pregunta que se ha contestado
    if request.method == "POST" and "btn_terminar" in request.POST:
        calificacion = 0
        for x in request.session["lista" + ide_cuestionario]:
            for n in x["preguntas"]:
                print(n)
                if str(n["correcta"]) == "true":
                    calificacion = calificacion + 1
        request.session["calificacion" + ide_cuestionario] = calificacion
        request.session["cuestionario_terminado" + ide_cuestionario] = True

    if request.method == "POST" and "btn_nuevocuestionario" in request.POST:
        del request.session["cuestionario_iniciado" + ide_cuestionario]

    if request.method == "POST" and "btn_cambiarestado" in request.POST:
        request.session["bloqueo"] = request.POST["bloqueo"]
        calificacion = 0
        for x in request.session["lista" + ide_cuestionario]:
            for n in x["preguntas"]:
                if int(n["contador"]) == int(request.POST["numero_pregunta"]):
                    n["llena"] = True
                    n["correcta"] = request.POST["correcta"]
                    n["opcion"] = request.POST["id_opciones"]
                if str(n["correcta"]) == "true":
                    calificacion = calificacion + 1
            request.session["calificacion" + ide_cuestionario] = calificacion
    # for x in request.session['lista']:
    # 	for n in x['preguntas']:
    # 		print(n)
    # 		print("----------")
    ctx = {
        "cuestionario_terminado": request.session[
            "cuestionario_terminado" + ide_cuestionario
        ],
        "calificacion": request.session["calificacion" + ide_cuestionario],
        "categorias": categorias,
        "lista": request.session["lista" + ide_cuestionario],
        "btn_terminar": request.session["bloqueo"],
        "total": request.session["total" + ide_cuestionario],
        "ide_cuestionario": ide_cuestionario,
    }
    return render(request, "cuestionario/cuestionario.html", ctx)


from easy_thumbnails.files import get_thumbnailer


def pregunta_ajax(request, id_preguntas, cuestionario):
    preguntas = Pregunta.objects.get(pk=id_preguntas).pregunta
    lista = []
    opciones = Respuesta.objects.filter(id_pregunta=id_preguntas)
    # .values(
    #     "respuesta", "correcta", "imagen", "imagen_crop", "id_opciones"
    # )
    for c in opciones:
        # print(c["imagen_crop"])
        try:
            imagen_crop = (
                get_thumbnailer(c.imagen)
                .get_thumbnail(
                    {
                        "size": (300, 150),
                        "box": c.imagen_crop,
                        "crop": False,
                        "detail": True,
                    }
                )
                .url
            )
        except Exception as e:
            imagen_crop = "none"
        lista.append(
            {
                "enunciado": c.respuesta,
                "correcta": c.valorRta,
                "imagen": imagen_crop,
                "id_opciones": c.pk,
            }
        )
    ctx = {
        "pregunta": preguntas,
        "opciones": list(lista),
        "cuestionario_terminado": request.session[
            "cuestionario_terminado" + str(cuestionario)
        ],
    }
    return JsonResponse(ctx, safe=False)
