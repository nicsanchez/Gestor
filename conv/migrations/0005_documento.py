# Generated by Django 2.2.4 on 2019-08-20 04:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conv', '0004_auto_20190818_1924'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('documento', models.FileField(null=True, upload_to='', verbose_name='Documento')),
                ('description', models.TextField(max_length=400, null=True, verbose_name='Descripción')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha de edición')),
                ('id_conv', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conv.Convocatoria')),
            ],
            options={
                'verbose_name': 'Documento',
                'verbose_name_plural': 'Documentos',
                'ordering': ['id_conv'],
            },
        ),
    ]
