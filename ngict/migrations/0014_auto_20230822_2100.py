# Generated by Django 3.2.19 on 2023-08-22 21:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ngict', '0013_auto_20230821_0138'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ('-course_title',), 'verbose_name_plural': 'Course'},
        ),
        migrations.RenameField(
            model_name='course',
            old_name='title',
            new_name='course_title',
        ),
        migrations.RenameField(
            model_name='lesson',
            old_name='title',
            new_name='lesson_title',
        ),
        migrations.RenameField(
            model_name='module',
            old_name='title',
            new_name='module_title',
        ),
        migrations.RenameField(
            model_name='resource',
            old_name='title',
            new_name='resource_title',
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ngict.question'),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ngict.course'),
        ),
        migrations.AlterField(
            model_name='assessmentscore',
            name='assessment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ngict.assessment'),
        ),
        migrations.AlterField(
            model_name='assessmentscore',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ngict.module'),
        ),
        migrations.AlterField(
            model_name='module',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ngict.course'),
        ),
        migrations.AlterField(
            model_name='question',
            name='assessment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ngict.assessment'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ngict.lesson'),
        ),
        migrations.AlterField(
            model_name='student',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='username',
            field=models.ForeignKey(max_length=20, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usercode',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_title', models.CharField(max_length=200)),
                ('project_description', models.CharField(max_length=200)),
                ('live_link', models.URLField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ngict.course')),
            ],
            options={
                'unique_together': {('course', 'project_title')},
            },
        ),
    ]
