# Generated by Django 2.2 on 2020-01-27 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appWeb', '0002_auto_20200106_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipocuest',
            name='id_tipoUsr',
            field=models.ForeignKey(db_column='id_tipoUsr', default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='appWeb.TipoUsr', verbose_name='Tipo de usuario:'),
            preserve_default=False,
        ),
    ]
