# Generated by Django 2.2.4 on 2020-03-13 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('create', '0014_auto_20200313_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='lineasemillero',
            name='id_coo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='create.Integrante', verbose_name='Coordinador'),
        ),
    ]
