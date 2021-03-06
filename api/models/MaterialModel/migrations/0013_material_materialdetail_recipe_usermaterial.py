# Generated by Django 3.2.5 on 2021-08-08 22:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MaterialModel', '0012_auto_20210808_2248'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_id', models.IntegerField(unique=True, verbose_name='物资id')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='物资名')),
            ],
        ),
        migrations.CreateModel(
            name='MaterialDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productivity', models.FloatField(verbose_name='物资自身产能')),
                ('level', models.SmallIntegerField(choices=[(1, 'Q1'), (2, 'Q2'), (3, 'Q3')], default=1, verbose_name='物资等级')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MaterialModel.material', verbose_name='物资')),
            ],
            options={
                'unique_together': {('material', 'level')},
            },
        ),
        migrations.CreateModel(
            name='UserMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.FloatField(verbose_name='拥有数量')),
                ('material_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MaterialModel.materialdetail', verbose_name='物资详情')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'unique_together': {('user', 'material_detail')},
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('needed_count', models.FloatField(verbose_name='所需数量')),
                ('produce_count', models.FloatField(default=1, verbose_name='产出物资数量')),
                ('material_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_detail', to='MaterialModel.materialdetail', verbose_name='产出详情')),
                ('raw_material_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='raw_material_detail', to='MaterialModel.materialdetail', verbose_name='所需物资详情')),
            ],
            options={
                'unique_together': {('material_detail', 'raw_material_detail')},
            },
        ),
    ]
