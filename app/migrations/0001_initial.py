# Generated by Django 5.0.2 on 2024-05-20 17:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('price_per_person', models.IntegerField()),
                ('popular', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.category')),
            ],
        ),
        migrations.CreateModel(
            name='Destination_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discription', models.TextField()),
                ('main_image', models.ImageField(upload_to='mymedia')),
                ('image2', models.ImageField(blank=True, upload_to='mymedia')),
                ('image3', models.ImageField(blank=True, upload_to='mymedia')),
                ('image4', models.ImageField(blank=True, upload_to='mymedia')),
                ('has_wifi', models.BooleanField(default=True)),
                ('has_dinner', models.BooleanField(default=True)),
                ('has_tub', models.BooleanField(default=True)),
                ('has_pool', models.BooleanField(default=True)),
                ('destinationid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.destination')),
            ],
        ),
    ]
