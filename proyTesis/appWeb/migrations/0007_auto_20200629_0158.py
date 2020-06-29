# Generated by Django 2.2 on 2020-06-29 01:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appWeb', '0006_auto_20200201_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nivel',
            name='id_competencia',
            field=models.ForeignKey(db_column='id_competencia', on_delete=django.db.models.deletion.DO_NOTHING, related_name='nivel', to='appWeb.Competencia', verbose_name='Competencia digital:'),
        ),
        migrations.CreateModel(
            name='HistoricoEvaluacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')),
                ('slug', models.SlugField(editable=False)),
                ('id_usr', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Respuesta realizada por:')),
            ],
            options={
                'verbose_name': 'Respuestas Usuario',
            },
        ),
    ]
