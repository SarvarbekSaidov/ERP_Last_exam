# Generated by Django 5.1.3 on 2024-12-02 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_lesson_liked_delete_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='liked',
        ),
        migrations.AddField(
            model_name='comment',
            name='liked',
            field=models.IntegerField(blank=True, choices=[(1, 'Like'), (0, 'Dislike')], null=True),
        ),
    ]