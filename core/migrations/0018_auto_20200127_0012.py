# Generated by Django 2.2.4 on 2020-01-27 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20200127_0010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='noticia',
            name='image',
        ),
        migrations.AddField(
            model_name='noticia',
            name='imagen',
            field=models.FileField(null=True, upload_to='', verbose_name='Imagen'),
        ),
    ]