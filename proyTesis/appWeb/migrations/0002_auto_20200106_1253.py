# Generated by Django 2.2 on 2020-01-06 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appWeb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='estado_codigo',
            field=models.BooleanField(null=True),
        ),
    ]
