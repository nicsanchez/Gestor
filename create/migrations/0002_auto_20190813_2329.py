# Generated by Django 2.2.4 on 2019-08-14 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('create', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semillero',
            name='id_group',
            field=models.CharField(choices=[('1', 'SISTEMIC')], max_length=50, null=True, verbose_name='Grupo'),
        ),
        migrations.AlterField(
            model_name='semillero',
            name='lines',
            field=models.CharField(choices=[('1', 'Linea 1')], max_length=50, null=True, verbose_name='Líneas de investigación'),
        ),
    ]
