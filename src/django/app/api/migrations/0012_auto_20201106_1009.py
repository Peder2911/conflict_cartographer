# Generated by Django 3.1.2 on 2020-11-06 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_project_long_description'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Project',
            new_name='ProjectDescription',
        ),
    ]