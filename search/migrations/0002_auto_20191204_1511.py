# Generated by Django 2.2.5 on 2019-12-04 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='New_camera_type_db',
            fields=[
                ('camera_type', models.CharField(max_length=70, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='New_location_db',
            fields=[
                ('location', models.CharField(max_length=70, primary_key=True, serialize=False)),
            ],
        ),
        migrations.DeleteModel(
            name='NewCameraTypeDb',
        ),
        migrations.DeleteModel(
            name='NewLocationDb',
        ),
    ]
