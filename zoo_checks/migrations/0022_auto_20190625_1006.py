# Generated by Django 2.2.2 on 2019-06-25 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zoo_checks', '0021_auto_20190624_1444'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='species',
            options={'ordering': ['common_name'], 'verbose_name_plural': 'species'},
        ),
    ]