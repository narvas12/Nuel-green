# Generated by Django 4.2.5 on 2023-12-17 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ngict', '0015_visitor'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='is_connected',
            field=models.BooleanField(default=False),
        ),
    ]