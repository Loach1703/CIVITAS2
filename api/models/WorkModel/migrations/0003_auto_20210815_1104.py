# Generated by Django 3.2.4 on 2021-08-15 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WorkModel', '0002_alter_sideline_record_every_sideline_all'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sideline_record',
            name='every_sideline_all',
        ),
        migrations.AddField(
            model_name='sideline_work',
            name='sideline_hunger',
            field=models.CharField(blank=True, default=4, max_length=20, verbose_name='饥饿消耗,不设置默认4'),
        ),
        migrations.AlterField(
            model_name='sideline_work',
            name='sideline_energy',
            field=models.CharField(blank=True, default=15, max_length=20, verbose_name='精力消耗,不设置默认15'),
        ),
        migrations.AlterField(
            model_name='sideline_work',
            name='sideline_happy',
            field=models.CharField(blank=True, default=3, max_length=20, verbose_name='快乐消耗,不设置默认3'),
        ),
        migrations.AlterField(
            model_name='sideline_work',
            name='sideline_health',
            field=models.CharField(blank=True, default=3, max_length=20, verbose_name='健康消耗,不设置默认3'),
        ),
        migrations.AlterField(
            model_name='sideline_work',
            name='sideline_skills_increase',
            field=models.CharField(blank=True, max_length=100, verbose_name='各技能增长修正，以空格隔开，不设置默认为1，设置需要全部都设置'),
        ),
    ]
