# Generated by Django 2.2.5 on 2019-12-04 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0006_authuser_db'),
    ]

    operations = [
        migrations.CreateModel(
            name='New_role_db',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=70)),
            ],
        ),
    ]