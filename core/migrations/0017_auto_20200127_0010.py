# Generated by Django 2.2.4 on 2020-01-27 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20200126_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='image',
            field=models.CharField(max_length=30, null=True, verbose_name='Imagen'),
        ),
    ]