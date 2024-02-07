# Generated by Django 3.2.19 on 2023-09-05 00:44

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('instructors', '0005_auto_20230904_2141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='description',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='lesson_title',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='order',
        ),
        migrations.AddField(
            model_name='lesson',
            name='created_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='lesson',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='content',
            field=ckeditor.fields.RichTextField(null=True),
        ),
    ]
