# Generated by Django 2.2 on 2020-10-18 23:35

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appWeb', '0014_auto_20201018_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area_competencia',
            name='info_text',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=17500),
        ),
        migrations.AlterField(
            model_name='competencia',
            name='info_text',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=17500),
        ),
        migrations.AlterField(
            model_name='pregunta',
            name='pregunta',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=17500),
        ),
    ]
