# Generated by Django 2.2.4 on 2020-05-11 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('create', '0016_auto_20200420_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='semillero',
            name='goals',
            field=models.TextField(null=True, verbose_name='Objetivos'),
        ),
        migrations.AddField(
            model_name='semillero',
            name='history',
            field=models.TextField(null=True, verbose_name='Antesedentes'),
        ),
        migrations.AddField(
            model_name='semillero',
            name='mision',
            field=models.TextField(null=True, verbose_name='Misión'),
        ),
        migrations.AddField(
            model_name='semillero',
            name='vision',
            field=models.TextField(null=True, verbose_name='Visión'),
        ),
    ]
