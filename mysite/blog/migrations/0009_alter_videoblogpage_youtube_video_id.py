# Generated by Django 5.1.7 on 2025-04-19 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_videoblogpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoblogpage',
            name='youtube_video_id',
            field=models.URLField(max_length=30),
        ),
    ]
