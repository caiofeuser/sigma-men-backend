# Generated by Django 5.0.6 on 2024-05-27 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_api', '0002_customusermodel_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='customusermodel',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
