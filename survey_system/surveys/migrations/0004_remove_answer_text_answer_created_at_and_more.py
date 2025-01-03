# Generated by Django 5.1.4 on 2024-12-06 17:12

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0003_alter_answer_choice_alter_survey_max_participants_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='text',
        ),
        migrations.AddField(
            model_name='answer',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='answer',
            name='choice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.choice'),
        ),
    ]
