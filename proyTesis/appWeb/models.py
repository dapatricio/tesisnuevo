from django.db import models
import hashlib
from django.contrib.auth.models import User

# Create your models here.
#
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from image_cropping import ImageCropField, ImageRatioField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify


class Area(models.Model):
    id_area = models.AutoField(primary_key=True)
    nombArea = models.CharField(
        max_length=250, verbose_name="Nombre del área academica:"
    )

    class Meta:
        verbose_name = "Áreas académica"
        db_table = "area"

    def __str__(self):
        return "%s" % self.nombArea


class Area_Competencia(models.Model):
    id_area_competencia = models.AutoField(primary_key=True)
    nombAreaCompetencia = models.CharField(
        max_length=250, verbose_name="Nombre del área de competencia:"
    )
    detalle_area_competencia = models.CharField(
        max_length=500, verbose_name="Descripcion del área de competencia:"
    )
    image = models.ImageField(upload_to="area-competencia", blank=True)
    info_text = RichTextUploadingField(max_length=17500)

    class Meta:
        verbose_name = "Áreas de competencia"
        db_table = "area_competencia"

    def __str__(self):
        return "%s" % self.nombAreaCompetencia


class TipoCuest(models.Model):
    id_tipoCuest = models.AutoField(primary_key=True)
    nombCuest = models.CharField(max_length=250, verbose_name="Tipo de cuestionario:")
    id_tipoUsr = models.ForeignKey(
        "TipoUsr",
        models.DO_NOTHING,
        db_column="id_tipoUsr",
        verbose_name="Tipo de usuario:",
    )

    class Meta:
        db_table = "tipoCuest"
        verbose_name = "Tipos de cuestionario"

    def __str__(self):

        return "%s" % self.nombCuest


class TipoDep(models.Model):
    id_tipoDep = models.AutoField(primary_key=True)
    tipo_dep = models.CharField(
        max_length=250, verbose_name="Nombre del tipo de dependencia:"
    )

    class Meta:
        verbose_name = "Tipos de dependencia"
        db_table = "tipoDep"

    def __str__(self):
        return "%s" % self.tipo_dep


class TipoUsr(models.Model):
    id_tipoUsr = models.AutoField(primary_key=True)
    tipo_usuario = models.CharField(
        max_length=250, verbose_name="Nombre del tipo de usuario:"
    )

    class Meta:
        verbose_name = "Tipos de usuario"
        db_table = "tipoUsr"

    def __str__(self):
        return "%s" % self.tipo_usuario


class Dependencia(models.Model):
    id_dependencia = models.AutoField(primary_key=True)
    nombDependencia = models.CharField(
        max_length=250, verbose_name="Nombre de la dependencia:"
    )

    id_tipoDep = models.ForeignKey(
        TipoDep,
        models.DO_NOTHING,
        db_column="id_tipoDep",
        verbose_name="Tipo de dependencia:",
    )
    id_area = models.ForeignKey(
        Area, models.DO_NOTHING, db_column="id_area", verbose_name="Área academica:"
    )

    class Meta:
        verbose_name = "Dependencias académica"
        db_table = "dependencia"

    def __str__(self):
        return "%s" % self.nombDependencia


class Competencia(models.Model):
    id_competencia = models.AutoField(primary_key=True)
    nombCompetencia = models.CharField(
        max_length=250, verbose_name="Nombre de la competencia:"
    )
    detalle_competencia = models.CharField(
        max_length=250, verbose_name="Descripción de la competencia:"
    )

    id_area_competencia = models.ForeignKey(
        Area_Competencia,
        models.DO_NOTHING,
        db_column="id_area_competencia",
        verbose_name="Área de la competencia:",
    )
    image = models.ImageField(upload_to="img-competencia", blank=True)
    info_text = RichTextUploadingField(max_length=17500)

    class Meta:
        verbose_name = "Competencias digitale"
        db_table = "competencia"

    def __str__(self):
        return "%s" % self.nombCompetencia


class Recomendaciones(models.Model):
    competencia = models.ForeignKey(
        Competencia, on_delete=models.DO_NOTHING, related_name="subida_nivel",
    )
    nivel = models.CharField(
        max_length=128,
        choices=(
            ("Basico", "Basico"),
            ("Intermedio", "Intermedio"),
            ("Avanzado", "Avanzado"),
        ),
    )
    contenido = models.TextField()

    class Meta:
        verbose_name = "Recomendacion para subir de nivel"
        verbose_name_plural = "Recomendacion para subir de nivel"
        unique_together = ["competencia", "nivel"]

    def __str__(self):
        return "%s" % self.competencia


class Pregunta(models.Model):
    id_pregunta = models.AutoField(primary_key=True)

    id_competencia = models.ForeignKey(
        Competencia,
        models.DO_NOTHING,
        db_column="id_competencia",
        verbose_name="Competencia digital a la que pertenece:",
    )
    id_tipoCuest = models.ForeignKey(
        TipoCuest,
        models.DO_NOTHING,
        db_column="id_tipoCuest",
        verbose_name="Tipo de cuestionario:",
    )

    ayuda = models.CharField(
        max_length=250, verbose_name="Instrucción para la pregunta:"
    )
    pregunta = RichTextUploadingField(max_length=17500)

    class Meta:
        verbose_name = "Pregunta"
        db_table = "pregunta"

    def __str__(self):
        return "%s" % self.pregunta


class Recomendacion(models.Model):
    id_recomendacion = models.AutoField(primary_key=True)
    recomendacion = models.CharField(
        max_length=500, verbose_name="Recomendación del valor respuesta:"
    )
    valor = models.IntegerField(verbose_name="Valor de la recomendación:")

    id_competencia = models.ForeignKey(
        Competencia,
        models.DO_NOTHING,
        db_column="id_competencia",
        verbose_name="Competencia a la que pertenece:",
    )

    class Meta:
        verbose_name = "Recomendacióne"
        db_table = "recomendacion"

    def __str__(self):
        return "%s" % self.recomendacion


class Respuesta(models.Model):
    id_respuesta = models.AutoField(primary_key=True)
    respuesta = models.CharField(
        max_length=250, blank=True, verbose_name="Respuesta pregunta:"
    )
    valorRta = models.IntegerField(verbose_name="Valor de la respuesta:")
    imagen = ImageCropField(max_length=150, upload_to="cursos", blank=True)
    imagen_crop = ImageRatioField(
        "imagen", "200x200", size_warning=True, free_crop=True
    )

    id_pregunta = models.ForeignKey(
        Pregunta,
        models.DO_NOTHING,
        db_column="id_pregunta",
        verbose_name="Pregunta a la que pertenece:",
    )

    class Meta:
        verbose_name = "Respuesta"
        db_table = "respuesta"

    def __str__(self):
        return "%s" % self.respuesta


class HistoricoEvaluacion(models.Model):
    id_usr = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="user_id",
        verbose_name="Respuesta realizada por:",
    )
    nombre_cuestionario = models.CharField(max_length=256, blank=True)
    code_uuid = models.CharField(max_length=32, blank=True)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha Creación")
    slug = models.SlugField(editable=False)

    class Meta:
        verbose_name = "Historial evaluaciones"

    def save(self, *args, **kwargs):
        """Se reescribe el método save para guardar el slug"""
        self.slug = slugify(f"{self.create_date}-{self.id_usr}")
        super().save(*args, **kwargs)

    def __str__(self):
        return "%s - %s" % (self.create_date, self.id_usr)


class RtaUsr(models.Model):
    id_rtaUser = models.AutoField(primary_key=True)
    rtaUser = models.IntegerField(verbose_name="Respuesta usuario")
    historico = models.ForeignKey(HistoricoEvaluacion, models.DO_NOTHING)

    id_pregunta = models.ForeignKey(
        Pregunta,
        models.DO_NOTHING,
        db_column="id_pregunta",
        verbose_name="Pregunta a la que pertenece:",
    )
    id_usr = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="user_id",
        verbose_name="Respuesta realizada por:",
    )

    class Meta:
        verbose_name = "Respuestas Usuario"
        db_table = "rtaUser"

    def __str__(self):
        return "%s" % self.rtaUser


class Nivel(models.Model):
    id_nivel = models.AutoField(primary_key=True)
    nivel = models.IntegerField(verbose_name="Nivel recomendado:")

    id_competencia = models.ForeignKey(
        Competencia,
        models.DO_NOTHING,
        db_column="id_competencia",
        verbose_name="Competencia digital:",
        related_name="nivel",
    )
    id_dependencia = models.ForeignKey(
        Dependencia,
        models.DO_NOTHING,
        db_column="id_dependencia",
        verbose_name="Dependencia:",
    )

    class Meta:
        verbose_name = "Niveles requerido"
        db_table = "nivel"

    def __str__(self):
        return "%s" % self.nivel


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cedula = models.CharField(max_length=11, verbose_name="Cédula usuario:")
    codigo = models.CharField(max_length=75, verbose_name="Codigo:")

    estado_codigo = models.BooleanField(null=True)

    id_tipoUsr = models.ForeignKey(
        TipoUsr,
        models.DO_NOTHING,
        db_column="id_tipoUsr",
        verbose_name="Tipo de usuario:",
    )
    id_dependencia = models.ForeignKey(
        Dependencia,
        models.DO_NOTHING,
        db_column="id_dependencia",
        verbose_name="Dependencia:",
    )
    genero = models.CharField(
        max_length=32,
        choices=(
            ("másculino", "másculino"),
            ("Femenino", "Femenino"),
            ("Otro", "Otro"),
        ),
        blank=True,
    )
    ancho_banda = models.CharField(
        max_length=32,
        choices=(
            ("10Mb", "10Mb"),
            ("15Mb", "15Mb"),
            ("más de 25mb", "más de 25mb"),
            ("más de 50mb", "más de 50mb"),
        ),
        verbose_name="Que ancho de banda de internet tiene?",
        blank=True,
    )
    tipo_computador = models.CharField(
        max_length=128,
        choices=(
            ("Computador de escritorio", "Computador de escritorio"),
            ("Laptop", "Laptop"),
        ),
        verbose_name="Que tipo de computador utiliza?",
        blank=True,
    )
    tiempo_dispositivo_movil = models.CharField(
        max_length=32,
        choices=(
            ("4h", "4h"),
            ("6h", "6h"),
            ("8h", "8h"),
            ("más de 10h", "más de 10h"),
        ),
        verbose_name="Cuanto tiempo al dia utiliza un dispositivo movil?",
        blank=True,
    )
    tipo_movil = models.CharField(
        max_length=128,
        choices=(("Celular", "Celular"), ("Tablet", "Tablet")),
        verbose_name="Que tipo de dispositivo movil utiliza con más frecuencia?",
        blank=True,
    )
    numero_computador = models.CharField(
        max_length=128,
        choices=(
            ("1", "1"),
            ("2", "2"),
            ("más de 4", "más de 4"),
            ("más de 6", "más de 6"),
        ),
        verbose_name="Cuantas computadores tiene en su domicilio?",
        blank=True,
    )
    numero_moviles = models.CharField(
        max_length=128,
        choices=(
            ("1", "1"),
            ("2", "2"),
            ("más de 4", "más de 4"),
            ("más de 6", "más de 6"),
        ),
        verbose_name="Cuantos dispositivos moviles tiene en su domicilio?",
        blank=True,
    )

    def __str__(self):
        return "%s" % self.user
