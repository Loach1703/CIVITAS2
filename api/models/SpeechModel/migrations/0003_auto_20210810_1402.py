# Generated by Django 3.2.5 on 2021-08-10 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SpeechModel', '0002_alter_speech_text'),
    ]

    operations = [
        migrations.DeleteModel(
            name='speech',
        ),
        migrations.DeleteModel(
            name='speech_attitude',
        ),
    ]
