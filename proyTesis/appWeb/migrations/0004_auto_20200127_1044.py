# Generated by Django 2.2 on 2020-01-27 10:44

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('appWeb', '0003_tipocuest_id_tipousr'),
    ]

    operations = [
        migrations.AddField(
            model_name='respuesta',
            name='imagen',
            field=image_cropping.fields.ImageCropField(blank=True, max_length=150, upload_to='cursos'),
        ),
        migrations.AddField(
            model_name='respuesta',
            name='imagen_crop',
            field=image_cropping.fields.ImageRatioField('imagen', '200x200', adapt_rotation=False, allow_fullsize=False, free_crop=True, help_text=None, hide_image_field=False, size_warning=True, verbose_name='imagen crop'),
        ),
    ]
