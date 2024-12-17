# Generated by Django 3.1.2 on 2020-10-30 11:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('refkey', models.CharField(max_length=32, unique=True)),
                ('mailed', models.BooleanField()),
                ('metadata', models.JSONField()),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invitation', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
