# Generated by Django 2.2 on 2020-09-09 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appWeb", "0009_auto_20200909_1701"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicoevaluacion",
            name="code_uuid",
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AddField(
            model_name="historicoevaluacion",
            name="nombre_cuestionario",
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
