# Generated by Django 2.2.5 on 2019-12-04 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0004_new_camera_type_db_new_location_db'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cameradb',
            name='id',
        ),
        migrations.RemoveField(
            model_name='cameradb',
            name='port_number',
        ),
        migrations.AddField(
            model_name='cameradb',
            name='camera_type',
            field=models.CharField(default='IP', max_length=70),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cameradb',
            name='ip_address',
            field=models.CharField(max_length=30, primary_key=True, serialize=False),
        ),
    ]
