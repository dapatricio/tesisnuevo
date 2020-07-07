from django.views.generic import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, reverse, redirect


class CategoriaTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "cuestionario/categorias.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_area_competencia = Area_Competencia.objects.all()
        context.update({"object_area": object_area_competencia})
        return context


class HistorialTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "cuestionario/historico.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_historico = HistoricoEvaluacion.objects.filter(
            id_usr=self.request.user
        ).order_by("-create_date")
        object_area_competencia = Area_Competencia.objects.all()
        context.update({"object_area": object_area_competencia})
        context.update({"object_historico": object_historico})
        return context


@login_required
def cuestionarios(request, **kwargs):
    lista = []
    area_competencia = kwargs.get("uuid")
    profile = Profile.objects.get(user=request.user)
    ide_cuestionario = str(profile.id_tipoUsr.pk)
    categorias = TipoCuest.objects.filter(id_tipoUsr=profile.id_tipoUsr)
    contador, total = 0, 0
    ide_cuestionario = f"_{request.user}_{area_competencia}"
    if ("calificacion" + ide_cuestionario) not in request.session:
        request.session["bloqueo" + ide_cuestionario] = "true"
        request.session["cuestionario_terminado" + ide_cuestionario] = False
        request.session["calificacion" + ide_cuestionario] = 0
        request.session["total" + ide_cuestionario] = total

    if ("cuestionario_iniciado" + ide_cuestionario) not in request.session:
        request.session["bloqueo" + ide_cuestionario] = "true"
        request.session["calificacion" + ide_cuestionario] = 0
        request.session["cuestionario_terminado" + ide_cuestionario] = False
        for c in categorias:
            lista_preguntas = []
            preguntas = Pregunta.objects.filter(id_tipoCuest=c.pk).order_by("?")
            if area_competencia != "all":
                preguntas = preguntas.filter(
                    id_competencia__id_area_competencia__pk=area_competencia
                )
            for d in preguntas:
                contador = contador + 1
                total = 1 + total
                lista_preguntas.append(
                    {
                        "contador": contador,
                        "id_preguntas": d.pk,
                        "llena": False,
                        "correcta": "0",
                        "opcion": 0,
                    }
                )
            lista.append(
                {"categorias": c.nombCuest, "preguntas": lista_preguntas,}
            )
            request.session["cuestionario_iniciado" + ide_cuestionario] = True
        request.session["total" + ide_cuestionario] = total
        total = 0
        request.session["lista" + ide_cuestionario] = lista

    # Aqui guardo la instancia para que se guarde la pregunta que se ha contestado
    if request.method == "POST" and "btn_terminar" in request.POST:
        calificacion = 0
        objHistorico = HistoricoEvaluacion.objects.create(id_usr=request.user)
        for x in request.session["lista" + ide_cuestionario]:
            for n in x["preguntas"]:
                pg = Pregunta.objects.get(pk=n["id_preguntas"])
                RtaUsr.objects.create(
                    rtaUser=n["correcta"],
                    id_pregunta=pg,
                    id_usr=request.user,
                    historico=objHistorico,
                )
                if str(n["correcta"]) == "1":
                    calificacion = calificacion + 1
        request.session["calificacion" + ide_cuestionario] = calificacion
        request.session["cuestionario_terminado" + ide_cuestionario] = True

    if request.method == "POST" and "btn_nuevocuestionario" in request.POST:
        del request.session["cuestionario_iniciado" + ide_cuestionario]
        # return redirect("/cuestionario/categoria/")

    if request.method == "POST" and "btn_cambiarestado" in request.POST:
        request.session["bloqueo" + ide_cuestionario] = request.POST["bloqueo"]
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

    ctx = {
        "cuestionario_terminado": request.session[
            "cuestionario_terminado" + ide_cuestionario
        ],
        "calificacion": request.session["calificacion" + ide_cuestionario],
        "categorias": categorias,
        "lista": request.session["lista" + ide_cuestionario],
        "btn_terminar": request.session["bloqueo" + ide_cuestionario],
        "total": request.session["total" + ide_cuestionario],
        "ide_cuestionario": ide_cuestionario,
        "temporizador": (
            settings.TEMPORIZADOR_ALL
            if area_competencia == "all"
            else settings.TEMPORIZADOR
        ),
    }
    return render(request, "cuestionario/cuestionario.html", ctx)


from easy_thumbnails.files import get_thumbnailer


def pregunta_ajax(request, id_preguntas, cuestionario):
    lista = []
    preguntas = Pregunta.objects.get(pk=id_preguntas)
    opciones = Respuesta.objects.filter(id_pregunta=id_preguntas)
    for c in opciones:
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
        "area": preguntas.id_competencia.id_area_competencia.nombAreaCompetencia,
        "digital": preguntas.id_competencia.nombCompetencia,
        "pregunta": preguntas.pregunta,
        "ayuda": preguntas.ayuda,
        "ayuda": preguntas.ayuda,
        "opciones": list(lista),
        "cuestionario_terminado": request.session[
            "cuestionario_terminado" + str(cuestionario)
        ],
    }
    return JsonResponse(ctx, safe=False)


from django.db.models import Avg, Count, Min, Sum
from django.db.models import F
from django.db.models import OuterRef, Subquery
from django.db.models import Func
from django.db.models.functions import Round


def repuestas_usuario(request, **kwargs):

    lista = {
        0: "Basico",
        1: "Basico",
        2: "Intermedio",
        3: "Intermedio",
        4: "Avanzado",
    }
    profile = Profile.objects.get(user=request.user)
    query = RtaUsr.objects.filter(
        id_usr__profile__id_dependencia=profile.id_dependencia
    )
    querySet = RtaUsr.objects.filter(id_usr=request.user)
    if "area" in kwargs:
        area = kwargs.get("area")
        if area != "all":
            querySet = querySet.filter(
                id_pregunta__id_competencia__id_area_competencia=area
            )
    rpst = (
        querySet.order_by(
            "id_pregunta__id_competencia__id_area_competencia",
            "id_pregunta__id_competencia",
        )
        .values(competencia=F("id_pregunta__id_competencia__nombCompetencia"))
        .annotate(
            ide=F("id_pregunta__id_competencia__id_competencia"),
            sumatoria=Sum("rtaUser"),
            area=F(
                "id_pregunta__id_competencia__id_area_competencia__nombAreaCompetencia"
            ),
            recomendado=F("id_pregunta__id_competencia__nivel__nivel"),
        )
        .values("competencia", "ide", "sumatoria", "area", "recomendado")
    )
    list = []
    Rarea = []
    for value in rpst:
        ar = (
            query.filter(id_pregunta__id_competencia__id_competencia=value["ide"])
            .values("id_usr")
            .annotate(s=Sum("rtaUser"))
            .values("id_usr", "s")
            .aggregate(p=Round(Avg("s")))
        )
        try:

            list.append(
                {
                    "competencia": value["competencia"],
                    "sumatoria": lista[int(value["sumatoria"])],
                    "recomendado": lista[int(value["recomendado"])],
                    "area": lista[int(ar["p"])],
                }
            )
            Rarea.append(int(ar["p"]))
        except Exception as e:
            pass

    c = rpst.count()
    competencia = [f"C{value+1}" for value in range(c)]
    Rpersonal = [value["sumatoria"] for value in rpst]
    Rrecomendado = [value["recomendado"] for value in rpst]

    ctx = {
        "rpst": list,
        "lista": competencia,
        "resul_personal": Rpersonal,
        "resul_recomendado": Rrecomendado,
        "resul_area": Rarea,
    }
    return render(request, "cuestionario/base.html", ctx)
