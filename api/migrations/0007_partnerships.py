# Generated by Django 4.2.2 on 2024-05-07 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_result_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partnerships',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_button', models.BooleanField(default=False)),
            ],
        ),
    ]
