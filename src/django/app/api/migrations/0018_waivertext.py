# Generated by Django 3.1.2 on 2020-11-09 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20201109_1250'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaiverText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False, help_text='Is this model active? Only one model should be active.')),
                ('content', models.TextField(default='ENTER A WAIVER TEXT HERE')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
