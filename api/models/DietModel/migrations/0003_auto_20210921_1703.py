# Generated by Django 3.2.4 on 2021-09-21 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DietModel', '0002_diet_materialdetail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='名字')),
                ('Owner', models.IntegerField(db_index=True, verbose_name='拥有者')),
                ('health', models.FloatField(default=0.0, verbose_name='健康度')),
                ('Satiety', models.FloatField(default=0.0, verbose_name='饱食度')),
                ('acid', models.FloatField(default=0.0, verbose_name='酸')),
                ('salty', models.FloatField(default=0.0, verbose_name='咸')),
                ('sweet', models.FloatField(default=0.0, verbose_name='甜')),
                ('bitterness', models.FloatField(default=0.0, verbose_name='苦')),
                ('aroma', models.FloatField(default=0.0, verbose_name='味道度')),
            ],
        ),
        migrations.AddField(
            model_name='diet_materialdetail',
            name='acid',
            field=models.FloatField(default=0.0, verbose_name='酸'),
        ),
        migrations.AlterField(
            model_name='diet_materialdetail',
            name='Satiety',
            field=models.FloatField(default=0.0, verbose_name='饱食度'),
        ),
        migrations.AlterField(
            model_name='diet_materialdetail',
            name='aroma',
            field=models.FloatField(default=0.0, verbose_name='味道度'),
        ),
        migrations.AlterField(
            model_name='diet_materialdetail',
            name='bitterness',
            field=models.FloatField(default=0.0, verbose_name='苦'),
        ),
        migrations.AlterField(
            model_name='diet_materialdetail',
            name='health',
            field=models.FloatField(default=0.0, verbose_name='健康度'),
        ),
        migrations.AlterField(
            model_name='diet_materialdetail',
            name='salty',
            field=models.FloatField(default=0.0, verbose_name='咸'),
        ),
        migrations.AlterField(
            model_name='diet_materialdetail',
            name='sweet',
            field=models.FloatField(default=0.0, verbose_name='甜'),
        ),
    ]