# Generated by Django 5.0.2 on 2024-05-22 16:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_booknow_adults_alter_booknow_child_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination_detail',
            name='destinationid',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.destination'),
        ),
    ]