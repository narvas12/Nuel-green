# Generated by Django 3.2.19 on 2023-10-08 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructors', '0015_assessment_is_taken'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
    ]