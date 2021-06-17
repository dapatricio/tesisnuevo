# Django core
import functools
import ssl
import tempfile

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render, render, reverse
from django.template.loader import render_to_string
from django.views.generic import TemplateView, View, DetailView
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pyplot as plt
# Local apps
from django_weasyprint import WeasyTemplateResponse, WeasyTemplateResponseMixin
from django_weasyprint.utils import django_url_fetcher
from weasyprint import HTML

from .models import *

from datetime import datetime, timedelta


class CategoriaTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "cuestionario/categorias.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_area_competencia = Area_Competencia.objects.all()
        now = datetime.now()
        object_basic = HistoricoEvaluacion.objects.filter(
            id_usr=self.request.user, code_uuid="basic"
        ).order_by("create_date")
        object_all = HistoricoEvaluacion.objects.filter(
            id_usr=self.request.user, code_uuid="all"
        ).order_by("create_date")
        disabled_all = not object_basic.exists()
        disabled_area = not object_all.exists()
        context.update(
            {
                "object_area": object_area_competencia,
                "disabled_all": disabled_all,
                "disabled_area": disabled_area,
            }
        )

        format = "%Y-%m-%d %H:%M:%S.%f+00:00"
        # Date basic
        last_object_basic = object_basic.last()
        if last_object_basic:
            date_last = datetime.strptime(str(last_object_basic.create_date), format)
            date_last = date_last + timedelta(hours=24)
            basic = (date_last > now)
            if not basic:
                value = f"cuestionario_iniciado_{self.request.user}_basic"
                if value in self.request.session:
                    self.request.session[value] = False

            context.update({"basic": basic, "basic_date": date_last})

        # Date all
        last_object_all = object_all.last()
        if last_object_all:
            date_last_all = datetime.strptime(str(last_object_all.create_date), format)
            date_last_all = date_last_all + timedelta(hours=24)
            all = (date_last_all > now)
            if not all:
                value = f"cuestionario_iniciado_{self.request.user}_all"
                if value in self.request.session:
                    self.request.session[value] = False
            context.update({"all": all, "all_date": date_last_all})
        return context


class HistorialTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "cuestionario/historico.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_historico = HistoricoEvaluacion.objects.filter(
            id_usr=self.request.user
        ).order_by("-create_date")
        object_historico = object_historico.exclude(code_uuid="basic")
        object_area_competencia = Area_Competencia.objects.all()
        context.update(
            {
                "object_area": object_area_competencia,
                "object_historico": object_historico,
            }
        )
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
            if area_competencia != "all" and area_competencia != "basic":
                preguntas = preguntas.filter(
                    id_competencia__id_area_competencia__pk=area_competencia
                )

            if area_competencia == "basic":
                preguntas = PreguntaCuestionarioGeneral.objects.all().order_by("?")

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
            lista.append({"categorias": c.nombCuest, "preguntas": lista_preguntas})
            request.session["cuestionario_iniciado" + ide_cuestionario] = True
        request.session["total" + ide_cuestionario] = total
        total = 0
        request.session["lista" + ide_cuestionario] = lista

    # Aqui guardo la instancia para que se guarde la pregunta que se ha contestado
    if request.method == "POST" and "btn_terminar" in request.POST:
        calificacion = 0
        txt = None
        if area_competencia == "basic":
            txt = "Cuestionario General"

        if area_competencia == "all":
            txt = "Todas las áreas de competencias digitales"

        if txt is None:
            txt = Area_Competencia.objects.get(pk=area_competencia).nombAreaCompetencia

        objHistorico = HistoricoEvaluacion.objects.create(
            id_usr=request.user, nombre_cuestionario=txt, code_uuid=area_competencia
        )
        for x in request.session["lista" + ide_cuestionario]:
            for n in x["preguntas"]:
                if area_competencia != "basic":
                    pg = Pregunta.objects.get(pk=n["id_preguntas"])
                    RtaUsr.objects.create(
                        rtaUser=n["correcta"],
                        id_pregunta=pg,
                        id_usr=request.user,
                        historico=objHistorico,
                    )
                    if str(n["correcta"]) == "1":
                        calificacion = calificacion + 1
                else:
                    pg = PreguntaCuestionarioGeneral.objects.get(pk=n["id_preguntas"])
                    RtaUsrGeneral.objects.create(
                        rta_user=n["correcta"],
                        id_pregunta=pg,
                        id_usr=request.user,
                        historico=objHistorico,
                    )
                    if str(n["correcta"]):
                        calificacion = calificacion + 1

        request.session["calificacion" + ide_cuestionario] = calificacion
        request.session["cuestionario_terminado" + ide_cuestionario] = True

    if request.method == "POST" and "btn_nuevocuestionario" in request.POST:
        request.session["cuestionario_iniciado" + ide_cuestionario] = False

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

    status = True
    if area_competencia == "basic":
        status = False

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
        "status": status,
        "tipo": area_competencia,
    }
    if area_competencia == "basic":
        return render(request, "cuestionario/cuestionario2.html", ctx)
    return render(request, "cuestionario/cuestionario.html", ctx)


from easy_thumbnails.files import get_thumbnailer


def pregunta_ajax(request, id_preguntas, cuestionario, tipo):
    lista = []
    if tipo != "basic":
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
            "opciones": list(lista),
            "cuestionario_terminado": request.session[
                "cuestionario_terminado" + str(cuestionario)
                ],
        }
    else:
        preguntas = PreguntaCuestionarioGeneral.objects.get(pk=id_preguntas)
        opciones = RespuestaCuestionarioGeneral.objects.filter(pregunta=id_preguntas)
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
            "area": "Cuestionario General",
            "digital": "",
            "pregunta": preguntas.pregunta,
            "ayuda": preguntas.ayuda,
            "opciones": list(lista),
            "cuestionario_terminado": request.session[
                "cuestionario_terminado" + str(cuestionario)
                ],
        }
    return JsonResponse(ctx, safe=False)


from django.db.models import F, Func, OuterRef, Subquery, Avg, Count, Min, Sum
from django.db.models.functions import Round
from django.http import HttpResponseRedirect

def redirect_user_to_pdf(request):
    if request.method == "POST":
        value = 9
        return HttpResponseRedirect('/pdf/report/9/')



def repuestas_usuario(request, **kwargs):
    lista = {
        0: "Basico",
        1: "Basico",
        2: "Intermedio",
        3: "Intermedio",
        4: "Avanzado",
    }
    choices = {
        "Basico": 0,
        "Intermedio": 1,
        "Avanzado": 2,
    }
    choices2 = {
        0: "Basico",
        1: "Intermedio",
        2: "Avanzado",
    }

    area = kwargs.get("area", None)
    profile = Profile.objects.get(user=request.user)
    base_query = RtaUsr.objects.exclude(historico__code_uuid="basic")
    query = base_query.filter(id_usr__profile__id_dependencia=profile.id_dependencia)
    querySet = base_query.filter(id_usr=request.user)
    if area:
        if area == "all":
            querySet = querySet.filter(historico__code_uuid="all")
            query = query.filter(historico__code_uuid="all")
        else:
            querySet = querySet.filter(
                id_pregunta__id_competencia__id_area_competencia=area
            )
            query = RtaUsr.objects.filter(
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
    list, Rarea = [], []
    for value in rpst:
        ar = (
            query.filter(id_pregunta__id_competencia__id_competencia=value["ide"])
                .values("id_usr")
                .annotate(s=Sum("rtaUser"))
                .values("id_usr", "s")
                .aggregate(p=Round(Avg("s")))
        )
        try:
            id = value["ide"]
            nivel = int(choices[str(lista[int(value["sumatoria"])])]) + 1
            text = "Sin registro"
            if not nivel > 2:
                nivel = choices2[int(nivel)]
                recomendaciones = Recomendaciones.objects.filter(
                    competencia__id_competencia=id, nivel=nivel
                )
                if recomendaciones.exists():
                    text = recomendaciones.first().contenido
            else:
                text = "Alcanzo el nivel maximo en esta competencia"
            list.append(
                {
                    "competencia": value["competencia"],
                    "sumatoria": lista[int(value["sumatoria"])],
                    "recomendado": lista[int(value["recomendado"])],
                    "area": lista[int(ar["p"])],
                    "subir": text,
                }
            )
            Rarea.append(int(ar["p"]))
        except Exception as e:
            print(e)

    c = rpst.count()
    competencia = [f"C{value + 1}" for value in range(c)]
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


def ff(query):
    print("=====a====")
    for q in query:
        print(q)
    return True


def repuestas_usuario_historico(request, **kwargs):
    lista = {
        0: "Basico",
        1: "Basico",
        2: "Intermedio",
        3: "Intermedio",
        4: "Avanzado",
    }
    choices = {
        "Basico": 0,
        "Intermedio": 1,
        "Avanzado": 2,
    }
    choices2 = {
        0: "Basico",
        1: "Intermedio",
        2: "Avanzado",
    }

    id_historico = kwargs.get("pk", None)
    ojk = HistoricoEvaluacion.objects.get(pk=id_historico)
    profile = Profile.objects.get(user=request.user)
    base_query = RtaUsr.objects.exclude(historico__code_uuid="basic")
    query = base_query.filter(id_usr__profile__id_dependencia=profile.id_dependencia)
    querySet = base_query.filter(id_usr=request.user)
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
    list, Rarea = [], []
    counter_rpst = 0
    labels = []
    sumatoria = []
    recomendado_graph = []
    for value in rpst:
        counter_rpst += 1
        labels.append("C"+str(counter_rpst))
        ar = (
            query.filter(id_pregunta__id_competencia__id_competencia=value["ide"])
                .values("id_usr")
                .annotate(s=Sum("rtaUser"))
                .values("id_usr", "s")
                .aggregate(p=Round(Avg("s")))
        )
        try:
            id = value["ide"]
            nivel = int(choices[str(lista[int(value["sumatoria"])])]) + 1
            text = "Sin registro"
            if not nivel > 2:
                nivel = choices2[int(nivel)]
                recomendaciones = Recomendaciones.objects.filter(
                    competencia__id_competencia=id, nivel=nivel
                )
                if recomendaciones.exists():
                    text = recomendaciones.first().contenido
            else:
                text = "Alcanzo el nivel maximo en esta competencia"
            sumatoria.append(int(value["sumatoria"]))
            recomendado_graph.append(int(value["recomendado"]))
            list.append(
                {
                    "competencia": value["competencia"],
                    "sumatoria": lista[int(value["sumatoria"])],
                    "recomendado": lista[int(value["recomendado"])],
                    "area": lista[int(ar["p"])],
                    "subir": text,
                }
            )
            Rarea.append(int(ar["p"]))
        except Exception as e:
            print(e)

    c = rpst.count()
    competencia = [f"C{value + 1}" for value in range(c)]
    Rpersonal = [value["sumatoria"] for value in rpst]
    Rrecomendado = [value["recomendado"] for value in rpst]

    ctx = {
        "rpst": list,
        "lista": competencia,
        "resul_personal": Rpersonal,
        "resul_recomendado": Rrecomendado,
        "resul_area": Rarea,
        "id": id_historico
    }
    if request.method == "POST":
        print(sumatoria)
        print(recomendado_graph)
        labels = labels
        men_means = sumatoria
        women_means = recomendado_graph

        x = np.arange(len(labels))  # the label locations
        width = 0.25  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2, men_means, width, label='Nivel Obtenido')
        rects2 = ax.bar(x + width/2, women_means, width, label='Nivel Recomendado')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Nivel')
        ax.set_title('Nivel Obtenido vs Nivel Recomendado')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()
        plt.tick_params(labelsize=8)

        fig.tight_layout()

        #plt.show()
        fig.set_figheight(3.5)
        fig.set_figwidth(7)
        plt.savefig('../static/graphimages/saved_figure.png')
        pdf_id = request.POST.get("submit_btn")
        return redirect('pdf_report', pk=pdf_id)

    return render(request, "cuestionario/base.html", ctx)


class MyModelView(DetailView):
    # vanilla Django DetailView
    model = HistoricoEvaluacion
    template_name = 'report/pdf.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lista = {
            0: "Basico",
            1: "Basico",
            2: "Intermedio",
            3: "Intermedio",
            4: "Avanzado",
        }
        area_competencia = Area_Competencia.objects.all()
        competencia = Competencia.objects.all().order_by("id_area_competencia__pk")
        rtausr = RtaUsr.objects.filter(historico=self.object).order_by(
            "id_pregunta__id_competencia__id_area_competencia",
            "id_pregunta__id_competencia",
        ).values(
            competencia=F("id_pregunta__id_competencia__nombCompetencia")
        ).annotate(
            ide=F("id_pregunta__id_competencia__id_competencia"),
            sumatoria=Sum("rtaUser"),
            area=F(
                "id_pregunta__id_competencia__id_area_competencia__nombAreaCompetencia"
            )
        )
        rtas = []
        for rta in rtausr:
            rtas.append({
                "area": rta.get("area"),
                "competencia": rta.get("competencia"),
                "sumatoria": lista.get(rta.get("sumatoria", 0))
            })
        context.update({"area_competencia": area_competencia, "competencia": competencia, "rtausr": rtas})
        return context


class MyModelDownloadView(WeasyTemplateResponseMixin, MyModelView):
    # suggested filename (is required for attachment/download!)
    pdf_filename = 'reporte.pdf'
