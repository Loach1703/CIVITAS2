# Generated by Django 3.2.4 on 2021-09-21 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='diet_material',
            fields=[
                ('raw_material_id', models.IntegerField(default=0, primary_key=True, serialize=False, verbose_name='食材id')),
                ('material_id', models.IntegerField(verbose_name='物品id')),
                ('name', models.CharField(max_length=20, verbose_name='食材名')),
            ],
        ),
    ]