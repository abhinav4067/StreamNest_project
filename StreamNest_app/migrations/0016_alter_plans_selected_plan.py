# Generated by Django 5.0.4 on 2024-05-16 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StreamNest_app', '0015_plans'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plans',
            name='selected_plan',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
