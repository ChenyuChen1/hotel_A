# Generated by Django 3.0.6 on 2020-06-08 06:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Air_Condition', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('request_time', models.DateTimeField(primary_key=True, serialize=False, verbose_name='请求发出时间')),
                ('room_id', models.IntegerField(verbose_name='房间号')),
                ('current_temp', models.IntegerField(verbose_name='当前温度')),
                ('init_temp', models.IntegerField(verbose_name='初始化温度')),
                ('target_temp', models.IntegerField(default=26, verbose_name='目标温度')),
                ('fan_speed', models.IntegerField(choices=[(1, 'HIGH'), (2, 'MIDDLE'), (3, 'LOW')], default=2, verbose_name='风速')),
                ('state', models.IntegerField(choices=[(1, 'SERVING'), (2, 'WAITING'), (3, 'SHUTDOWN')], default=3, verbose_name='服务状态')),
                ('fee_rate', models.FloatField(default=0.8, verbose_name='费率')),
                ('fee', models.FloatField(default=0.0, verbose_name='费用')),
                ('serve_time', models.IntegerField(default=0, verbose_name='当前服务时长')),
                ('wait_time', models.IntegerField(default=0, verbose_name='当前等待时长')),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(choices=[(1, 'WORKING'), (2, 'FREE')], default=2, verbose_name='服务状态')),
                ('start_time', models.DateField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('serve_time', models.FloatField(verbose_name='服务时长')),
                ('room_id', models.IntegerField(verbose_name='服务房间号')),
                ('target_temp', models.IntegerField(verbose_name='目标温度')),
                ('fee', models.FloatField(verbose_name='费用')),
                ('fee_rate', models.FloatField(verbose_name='费率')),
                ('fan_speed', models.IntegerField(default=2, verbose_name='风速')),
            ],
        ),
        migrations.CreateModel(
            name='ServingQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serving_num', models.IntegerField(default=0, verbose_name='服务对象数')),
            ],
        ),
        migrations.CreateModel(
            name='StatisticController',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='WaitingQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waiting_num', models.IntegerField(default=0, verbose_name='等待对象数')),
            ],
        ),
        migrations.RemoveField(
            model_name='scheduler',
            name='request_num',
        ),
        migrations.RemoveField(
            model_name='scheduler',
            name='service_num',
        ),
        migrations.AlterField(
            model_name='scheduler',
            name='default_target_temp',
            field=models.IntegerField(default=26, verbose_name='默认目标温度'),
        ),
        migrations.AlterField(
            model_name='scheduler',
            name='fee_rate_h',
            field=models.FloatField(default=1.0, verbose_name='高风速费率'),
        ),
        migrations.AlterField(
            model_name='scheduler',
            name='fee_rate_l',
            field=models.FloatField(default=0.5, verbose_name='低风速费率'),
        ),
        migrations.AlterField(
            model_name='scheduler',
            name='fee_rate_m',
            field=models.FloatField(default=0.8, verbose_name='中风速费率'),
        ),
        migrations.AlterField(
            model_name='scheduler',
            name='state',
            field=models.IntegerField(choices=[(1, 'WORKING'), (2, 'SHUTDOWN'), (3, 'SETMODE'), (4, 'READY')], verbose_name='中控机状态'),
        ),
        migrations.AlterField(
            model_name='scheduler',
            name='temp_high_limit',
            field=models.IntegerField(default=0, verbose_name='最高温度限制'),
        ),
        migrations.AlterField(
            model_name='scheduler',
            name='temp_low_limit',
            field=models.IntegerField(default=0, verbose_name='最低温度限制'),
        ),
    ]
