# Generated by Django 4.2.2 on 2024-04-30 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_question_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='number_of_questions',
            field=models.IntegerField(default=0),
        ),
    ]