# Generated by Django 5.1.4 on 2024-12-06 18:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0005_survey_end_date_alter_answer_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='survey',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='surveys.survey'),
        ),
    ]
