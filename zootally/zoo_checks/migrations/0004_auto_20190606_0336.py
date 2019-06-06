# Generated by Django 2.2.1 on 2019-06-06 03:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zoo_checks', '0003_auto_20190606_0233'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='animalcount',
            options={'ordering': ['datetimecounted']},
        ),
        migrations.AlterModelOptions(
            name='speciescount',
            options={'ordering': ['datetimecounted']},
        ),
        migrations.RenameField(
            model_name='animalcount',
            old_name='datetime',
            new_name='datetimecounted',
        ),
        migrations.RenameField(
            model_name='speciescount',
            old_name='datetime',
            new_name='datetimecounted',
        ),
    ]
