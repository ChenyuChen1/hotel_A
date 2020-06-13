import os
import pathlib
import random
import sys
from datetime import timedelta
from datetime import datetime

import django
from faker import Faker
from django.utils import timezone

# 将项目根目录添加到 Python 的模块搜索路径中
back = os.path.dirname
BASE_DIR = back(back(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotel.settings")
    django.setup()

    from Air_Condition.models import Scheduler, Room

    from django.contrib.auth.models import User

    print('clean database')
    Room.objects.all().delete()

    print('create a fake detail')
    faker = Faker()
    for i in range(1000):
        """产生10000条数据"""
        request_id = i
        request_time = faker.date_time_between_dates(datetime(2017, 1, 1, 1, 1, 1), datetime.now())
        room_id = faker.random_int(min=0, max=4)
        current_temp = faker.random_int(min=20, max=30)
        init_temp = faker.random_int(min=20, max=30)
        target_temp = faker.random_int(min=20, max=30)
        fan_speed = faker.random_int(min=1, max=3)
        state = faker.random_int(min=1, max=4)
        fee_rate = 0.5
        fee = faker.random_int(min=0, max=999)
        serve_time = faker.random_int(min=1, max=99)
        wait_time = faker.random_int(min=0, max=30)
        operation = faker.random_int(min=1, max=4)
        scheduling_num = faker.random_int(min=1, max=30)
        detail = Room.objects.create(request_id=request_id,
                                     request_time=request_time,
                                     room_id=room_id,
                                     current_temp=current_temp,
                                     init_temp=init_temp,
                                     target_temp=target_temp,
                                     fan_speed=fan_speed,
                                     state=state,
                                     fee_rate=fee_rate,
                                     fee=fee,
                                     serve_time=serve_time,
                                     wait_time=wait_time,
                                     operation=operation,
                                     scheduling_num=scheduling_num)
        # print(detail.request_id)
        detail.save()

