# Generated by Django 3.2.5 on 2021-08-08 00:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('SkillModel', '0017_auto_20210808_0037'),
    ]

    operations = [
        migrations.CreateModel(
            name='BigSkill',
            fields=[
                ('id', models.SmallIntegerField(primary_key=True, serialize=False, verbose_name='大类技能id')),
                ('name', models.CharField(max_length=20, verbose_name='大类技能名称')),
            ],
        ),
        migrations.CreateModel(
            name='SmallSkill',
            fields=[
                ('subid', models.SmallIntegerField(primary_key=True, serialize=False, verbose_name='大类下的小类id')),
                ('name', models.CharField(max_length=20, verbose_name='小类名称')),
                ('sub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SkillModel.bigskill', verbose_name='所属大类')),
            ],
        ),
        migrations.CreateModel(
            name='UserSkill',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('big_level', models.SmallIntegerField(choices=[(1, '学徒'), (2, '匠人'), (3, '匠师'), (4, '专家'), (5, '大师'), (6, '宗师'), (7, '大宗师')], verbose_name='大类技能等级')),
                ('big_skillnum', models.FloatField(verbose_name='大类技能点')),
                ('small_skillnum', models.FloatField(verbose_name='小类技能点')),
                ('big_skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SkillModel.bigskill', verbose_name='大类技能')),
                ('small_skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SkillModel.smallskill', verbose_name='小类技能')),
            ],
        ),
    ]