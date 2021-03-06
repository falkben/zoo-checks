# Generated by Django 2.2.2 on 2019-06-07 16:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('zoo_checks', '0008_auto_20190607_1318'), ('zoo_checks', '0009_auto_20190607_1408'), ('zoo_checks', '0010_auto_20190607_1411'), ('zoo_checks', '0011_auto_20190607_1519'), ('zoo_checks', '0012_auto_20190607_1540'), ('zoo_checks', '0013_auto_20190607_1559'), ('zoo_checks', '0014_auto_20190607_1610'), ('zoo_checks', '0015_auto_20190607_1612'), ('zoo_checks', '0016_auto_20190607_1617')]

    dependencies = [
        ('zoo_checks', '0007_auto_20190606_1242'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='animalcount',
            name='users',
        ),
        migrations.RemoveField(
            model_name='speciescount',
            name='users',
        ),
        migrations.AddField(
            model_name='animal',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='animalcount',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='speciescount',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='animal',
            name='exhibit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='animals', to='zoo_checks.Exhibit'),
        ),
        migrations.AlterField(
            model_name='animalcount',
            name='exhibit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='zoo_checks.Exhibit'),
        ),
        migrations.AlterField(
            model_name='exhibit',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='speciescount',
            name='exhibit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='zoo_checks.Exhibit'),
        ),
        migrations.RemoveField(
            model_name='animal',
            name='accession_number',
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('active', models.BooleanField(default=True)),
                ('exhibit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='groups', to='zoo_checks.Exhibit')),
                ('species', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zoo_checks.Species')),
                ('accession_number', models.PositiveSmallIntegerField(unique=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GroupCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datecounted', models.DateField(auto_now=True)),
                ('count', models.PositiveSmallIntegerField(default=0)),
                ('exhibit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='zoo_checks.Exhibit')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zoo_checks.Group')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['datecounted'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='animal',
            name='accession_number',
            field=models.PositiveSmallIntegerField(unique=True),
        ),
    ]
