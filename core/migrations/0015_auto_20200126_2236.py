# Generated by Django 2.2.4 on 2020-01-27 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_noticia_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='description',
            field=models.TextField(null=True, verbose_name='Descripción'),
        ),
    ]