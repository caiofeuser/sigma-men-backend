# Generated by Django 5.0.6 on 2024-05-19 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_result_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='options',
            field=models.ManyToManyField(blank=True, null=True, related_name='options', to='api.option'),
        ),
    ]
