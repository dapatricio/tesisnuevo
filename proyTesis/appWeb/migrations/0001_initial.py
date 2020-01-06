# Generated by Django 2.2 on 2020-01-06 17:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id_area', models.AutoField(primary_key=True, serialize=False)),
                ('nombArea', models.CharField(max_length=250, verbose_name='Nombre del área academica:')),
            ],
            options={
                'verbose_name': 'Áreas académica',
                'db_table': 'area',
            },
        ),
        migrations.CreateModel(
            name='Area_Competencia',
            fields=[
                ('id_area_competencia', models.AutoField(primary_key=True, serialize=False)),
                ('nombAreaCompetencia', models.CharField(max_length=250, verbose_name='Nombre del área de competencia:')),
                ('detalle_area_competencia', models.CharField(max_length=500, verbose_name='Descripcion del área de competencia:')),
            ],
            options={
                'verbose_name': 'Áreas de competencia',
                'db_table': 'area_competencia',
            },
        ),
        migrations.CreateModel(
            name='Competencia',
            fields=[
                ('id_competencia', models.AutoField(primary_key=True, serialize=False)),
                ('nombCompetencia', models.CharField(max_length=250, verbose_name='Nombre de la competencia:')),
                ('detalle_competencia', models.CharField(max_length=250, verbose_name='Descripción de la competencia:')),
                ('id_area_competencia', models.ForeignKey(db_column='id_area_competencia', on_delete=django.db.models.deletion.DO_NOTHING, to='appWeb.Area_Competencia', verbose_name='Área de la competencia:')),
            ],
            options={
                'verbose_name': 'Competencias digitale',
                'db_table': 'competencia',
            },
        ),
        migrations.CreateModel(
            name='Dependencia',
            fields=[
                ('id_dependencia', models.AutoField(primary_key=True, serialize=False)),
                ('nombDependencia', models.CharField(max_length=250, verbose_name='Nombre de la dependencia:')),
                ('id_area', models.ForeignKey(db_column='id_area', on_delete=django.db.models.deletion.DO_NOTHING, to='appWeb.Area', verbose_name='Área academica:')),
            ],
            options={
                'verbose_name': 'Dependencias académica',
                'db_table': 'dependencia',
            },
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id_pregunta', models.AutoField(primary_key=True, serialize=False)),
                ('ayuda', models.CharField(max_length=250, verbose_name='Instrucción para la pregunta:')),
                ('pregunta', models.CharField(max_length=250, verbose_name='Pregunta:')),
                ('id_competencia', models.ForeignKey(db_column='id_competencia', on_delete=django.db.models.deletion.DO_NOTHING, to='appWeb.Competencia', verbose_name='Competencia digital a la que pertenece:')),
            ],
            options={
                'verbose_name': 'Pregunta',
                'db_table': 'pregunta',
            },
        ),
        migrations.CreateModel(
            name='TipoCuest',
            fields=[
                ('id_tipoCuest', models.AutoField(primary_key=True, serialize=False)),
                ('nombCuest', models.CharField(max_length=250, verbose_name='Tipo de cuestionario:')),
            ],
            options={
                'verbose_name': 'Tipos de cuestionario',
                'db_table': 'tipoCuest',
            },
        ),
        migrations.CreateModel(
            name='TipoDep',
            fields=[
                ('id_tipoDep', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_dep', models.CharField(max_length=250, verbose_name='Nombre del tipo de dependencia:')),
            ],
            options={
                'verbose_name': 'Tipos de dependencia',
                'db_table': 'tipoDep',
            },
        ),
        migrations.CreateModel(
            name='TipoUsr',
            fields=[
                ('id_tipoUsr', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_usuario', models.CharField(max_length=250, verbose_name='Nombre del tipo de usuario:')),
            ],
            options={
                'verbose_name': 'Tipos de usuario',
                'db_table': 'tipoUsr',
            },
        ),
        migrations.CreateModel(
            name='RtaUsr',
            fields=[
                ('id_rtaUser', models.AutoField(primary_key=True, serialize=False)),
                ('rtaUser', models.CharField(max_length=75, verbose_name='Respuesta usuario')),
                ('id_pregunta', models.ForeignKey(db_column='id_pregunta', on_delete=django.db.models.deletion.DO_NOTHING, to='appWeb.Pregunta', verbose_name='Pregunta a la que pertenece:')),
                ('id_usr', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Respuesta realizada por:')),
            ],
            options={
                'verbose_name': 'Respuestas Usuario',
                'db_table': 'rtaUser',
            },
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id_respuesta', models.AutoField(primary_key=True, serialize=False)),
                ('respuesta', models.CharField(max_length=250, verbose_name='Respuesta pregunta:')),
                ('valorRta', models.IntegerField(verbose_name='Valor de la respuesta:')),
                ('id_pregunta', models.ForeignKey(db_column='id_pregunta', on_delete=django.db.models.deletion.DO_NOTHING, to='appWeb.Pregunta', verbose_name='Pregunta a la que pertenece:')),
            ],
            options={
                'verbose_name': 'Respuesta',
                'db_table': 'respuesta',
            },
        ),
        migrations.CreateModel(
            name='Recomendacion',
            fields=[
                ('id_recomendacion', models.AutoField(primary_key=True, serialize=False)),
                ('recomendacion', models.CharField(max_length=500, verbose_name='Recomendación del valor respuesta:')),
                ('valor', models.IntegerField(verbose_name='Valor de la recomendación:')),
                ('id_competencia', models.ForeignKey(db_column='id_competencia', on_delete=django.db.models.deletion.DO_NOTHING, to='appWeb.Competencia', verbose_name='Competencia a la que pertenece:')),
            ],
            options={
                'verbose_name': 'Recomendacióne',
                'db_table': 'recomendacion',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(max_length=11, verbose_name='Cédula usuario:')),
                ('codigo', models.CharField(max_length=75, verbose_name='Codigo:')),
                ('estado_codigo', models.BooleanField()),
                ('id_dependencia', models.ForeignKey(db_column='id_dependencia', on_delete=django.db.models.deletion.DO_NOTHING, to='appWeb.Dependencia', verbose_name='Dependencia:')),
                ('id_tipoUsr', models.ForeignKey(db_column='id_tipoUsr', on_delete=django.db.models.deletion.DO_NOTHING, to='appWeb.TipoUsr', verbose_name='Tipo de usuario:')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='pregunta',
            name='id_tipoCuest',
            field=models.ForeignKey(db_column='id_tipoCuest', on_delete=django.db.models.deletion.DO_NOTHING, to='appWeb.TipoCuest', verbose_name='Tipo de cuestionario:'),
        ),
        migrations.CreateModel(
            name='Nivel',
            fields=[
                ('id_nivel', models.AutoField(primary_key=True, serialize=False)),
                ('nivel', models.IntegerField(verbose_name='Nivel recomendado:')),
                ('id_competencia', models.ForeignKey(db_column='id_competencia', on_delete=django.db.models.deletion.DO_NOTHING, to='appWeb.Competencia', verbose_name='Competencia digital:')),
                ('id_dependencia', models.ForeignKey(db_column='id_dependencia', on_delete=django.db.models.deletion.DO_NOTHING, to='appWeb.Dependencia', verbose_name='Dependencia:')),
            ],
            options={
                'verbose_name': 'Niveles requerido',
                'db_table': 'nivel',
            },
        ),
        migrations.AddField(
            model_name='dependencia',
            name='id_tipoDep',
            field=models.ForeignKey(db_column='id_tipoDep', on_delete=django.db.models.deletion.DO_NOTHING, to='appWeb.TipoDep', verbose_name='Tipo de dependencia:'),
        ),
    ]
