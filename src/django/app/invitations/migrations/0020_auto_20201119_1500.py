# Generated by Django 3.1.2 on 2020-11-19 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20201116_1616'),
        ('invitations', '0019_auto_20201119_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='countries',
            field=models.ManyToManyField(blank=True, help_text='Countries that will be assigned to the user once they complete registration', related_name='invited_assignees', to='api.Country'),
        ),
    ]