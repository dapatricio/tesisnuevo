# Generated by Django 2.2 on 2021-07-16 03:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appWeb', '0018_auto_20210715_2130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competencia',
            name='id_nivel',
        ),
    ]
