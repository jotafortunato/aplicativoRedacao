# Generated by Django 4.2.6 on 2024-05-22 03:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('appRedacao', '0002_alter_aluno_options_alter_correcao_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='senha',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='professor',
            name='senha',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='redacoes',
            name='data_envio',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('senha', models.CharField(max_length=8)),
                ('funcao', models.CharField(max_length=55)),
                ('id_aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appRedacao.aluno')),
                ('id_professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appRedacao.professor')),
            ],
        ),
    ]
