# Generated by Django 3.1.2 on 2020-11-02 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0005_remove_invitation_refkey'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='refkey',
            field=models.CharField(max_length=32, null=True),
        ),
    ]