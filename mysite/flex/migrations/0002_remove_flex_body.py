# Generated by Django 5.1.7 on 2025-03-17 22:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flex', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flex',
            name='body',
        ),
    ]
