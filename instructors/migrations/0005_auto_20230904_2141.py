# Generated by Django 3.2.19 on 2023-09-04 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructors', '0004_course_instructor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='id',
        ),
        migrations.AlterField(
            model_name='module',
            name='order',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]