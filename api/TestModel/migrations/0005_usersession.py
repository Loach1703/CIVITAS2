# Generated by Django 3.2.5 on 2021-07-23 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestModel', '0004_weather'),
    ]

    operations = [
        migrations.CreateModel(
            name='usersession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=20)),
                ('sessionid', models.CharField(max_length=32)),
            ],
        ),
    ]