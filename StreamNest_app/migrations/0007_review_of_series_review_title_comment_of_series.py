# Generated by Django 5.0.4 on 2024-05-15 13:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StreamNest_app', '0006_review_of_movies_review_of_series'),
    ]

    operations = [
        migrations.AddField(
            model_name='review_of_series',
            name='review_title',
            field=models.TextField(max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='comment_of_series',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_comment', models.TextField(max_length=500, null=True)),
                ('review_date', models.DateField(null=True)),
                ('episodes_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='StreamNest_app.episodes')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StreamNest_app.user_reg')),
            ],
        ),
    ]
